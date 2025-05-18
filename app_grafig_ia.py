import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

api_key = os.getenv('GEMINI_KEY')

if not api_key:
    print("Erro: Chave da API não encontrada no arquivo .env")
    exit(1)

# Configurando a API do Google Gemini
genai.configure(api_key=api_key)

try:
    # Usando o modelo diretamente sem imprimir informações extras
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    # Fazendo uma solicitação simples para testar a API
    prompt = "Esse texto se trata de uma transcrição de audio, voce deve melhorar essa frase e" \
    "dar sentido a ela, melhorando a pontuação, mudando palavras que estiverem erradas" \
    " e dando mais sentido para ele, lembrando que deve ser em português."

    # Obtendo e exibindo apenas a resposta
    response = model.generate_content(prompt)
    print(response.text)

except Exception as e:
    print(f"Erro: {e}")
