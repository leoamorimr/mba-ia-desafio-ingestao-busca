import sys
from search import search_prompt

def main():
    if len(sys.argv) < 2:
        question = input("Faça sua pergunta: ")
        if not question.strip():
            print("Pergunta não pode estar vazia.")
            return
    else:
        question = " ".join(sys.argv[1:])
    
    try:
        search_prompt(question=question)
    except Exception as e:
        print(f"Erro: {e}")
        return

if __name__ == "__main__":
    main()