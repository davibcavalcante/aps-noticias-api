import os
import numpy as np
import logging
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from src.nlp.preprocessing import clean_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminhos dos arquivos salvos
MODEL_PATH = "src/nlp/models/model.h5"
TOKENIZER_PATH = "src/nlp/models/tokenizer.pkl"
DATA_PATH = "src/data/data.json"
DATA_TEST_PATH = "src/data/data_test.json"

# Função para carregar o modelo treinado
def load_trained_model():
    try:
        model = load_model(MODEL_PATH)
        logger.info("Modelo carregado com sucesso.")
        return model
    except Exception as e:
        logger.error(f"Erro ao carregar o modelo: {e}")
        raise e  # Levanta o erro para garantir que o processo falhe corretamente

# Função para carregar o tokenizer salvo
def load_tokenizer():
    try:
        with open(TOKENIZER_PATH, 'rb') as f:
            tokenizer = pickle.load(f)
        logger.info("Tokenizer carregado com sucesso.")
        return tokenizer
    except Exception as e:
        logger.error(f"Erro ao carregar o tokenizer: {e}")
        raise e

# Função para fazer a predição de uma frase
def predict_class(text):
    model = load_trained_model()
    tokenizer = load_tokenizer()

    clean_input = clean_text(text)
    sequence = tokenizer.texts_to_sequences([clean_input])

    padded = pad_sequences(sequence, maxlen=50, padding='post', truncating='post')
    prediction = model.predict(padded)[0]
    
    labels = ["irrelevante", "boa", "ruim"]
    return labels[np.argmax(prediction)]

# Função para classificar várias notícias do JSON
def classify_all():
    try:
        logger.info("Carregando o modelo e tokenizer...")
        model = load_trained_model()
        tokenizer = load_tokenizer()

        logger.info(f"Modelo e tokenizer carregados com sucesso.")

        with open(DATA_TEST_PATH, 'r', encoding='utf-8') as f:
          data = json.load(f)

        results = []
        for entry in data:
            clean_text_input = clean_text(entry["text"])

            logger.info(f"Processando texto: {clean_text_input}")
            
            sequence = tokenizer.texts_to_sequences([clean_text_input])
            padded = pad_sequences(sequence, maxlen=50, padding='post', truncating='post')
            
            logger.info(f"Texto transformado para sequência.")

            # Prevendo a classificação
            prediction = model.predict(padded)[0]
            label = ["irrelevante", "boa", "ruim"][np.argmax(prediction)]
            results.append({"text": clean_text_input, "classificacao": label, "date": entry["date"], "tag": entry["tag"]})
        
        logger.info("Classificação concluída com sucesso.")
        return results

    except Exception as e:
        logger.error(f"Ocorreu um erro durante a classificação: {str(e)}")
        return {"error": str(e)}