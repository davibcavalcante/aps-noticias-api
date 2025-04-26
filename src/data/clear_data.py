import re
import string
import json
from unidecode import unidecode

# Stopwords que você quer remover
stopWords = ["a", "o", "e", "na", "no", "em", "da", "de", "para", "com", "sao", "um", "uma", "go", "to", "rs", "mt", "rj"]

# Função para limpar o texto
def limpar_texto(texto):
    texto = unidecode(texto)  # Remove acentos
    texto = re.sub(r'[0-9' + string.punctuation + 'ˆº]', '', texto)  # Remove números e pontuação
    texto = texto.lower()  # Deixa tudo minúsculo
    palavras = texto.split()
    palavras = [palavra for palavra in palavras if palavra not in stopWords and len(palavra) > 1]
    return " ".join(palavras)

# --- Aqui começa o fluxo principal ---

# Lendo o arquivo JSON
with open('data.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Limpando o campo texto
for item in dados:
    if 'text' in item:
        item['text'] = limpar_texto(item['text'])

# Salvando o resultado em outro arquivo JSON (ou sobrescrevendo o original)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)

print("Arquivo JSON limpo e salvo como 'data.json'.")
