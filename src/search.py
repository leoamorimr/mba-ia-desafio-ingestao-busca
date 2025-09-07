import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

for k in ("OPENAI_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set.")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
	if not question:
		raise ValueError("A pergunta não pode ser vazia.")  
  
	embeddings = OpenAIEmbeddings(
      model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small")
    )
    
	store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    
	results = store.similarity_search_with_score(question, k=10)
	
	if not results:
		print("Não tenho informações necessárias para responder sua pergunta.")
		return
	
	context_parts = []
	for doc, score in results:
		if score < 0.8:
			context_parts.append(doc.page_content.strip())
	
	if not context_parts:
		print("Não tenho informações necessárias para responder sua pergunta.")
		return
	
	context = "".join(context_parts)
	
	llm = ChatOpenAI(
		model=os.getenv("OPENAI_MODEL", "gpt-5-nano"),
		temperature=0.5
	)
	
	prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
	chain = prompt | llm
	
	response = chain.invoke({
		"contexto": context,
		"pergunta": question
	})
	
	print(response.content)