import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import os

nltk.data.path.append(os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'nltk_data'))

# Verificações
nltk.download('wordnet')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_text(text):
    # Converte o texto para minúsculas
    text = text.lower()
    
    # Tokeniza o texto (transforma em uma lista de palavras)
    tokens = word_tokenize(text)
    
    # Aplica a lematização
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Define as stopwords em português
    stop_words = set(stopwords.words('portuguese'))
    
    # Filtra tokens: exclui stopwords e pontuação
    words = [w for w in tokens if w not in stop_words and w not in string.punctuation]
    
    return words
