import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D, LSTM, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.regularizers import l2
from sklearn.utils.class_weight import compute_class_weight
from src.nlp.preprocessing import clean_text
from sklearn.metrics import classification_report
import os
import pickle

DATA_PATH = "src/data/data.json"
MODEL_PATH = "src/nlp/models/model.h5"
TOKENIZER_PATH = "src/nlp/models/tokenizer.pkl"

def train_model():
    # Carrega os dados
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [clean_text(item["text"]) for item in data]
    labels = [item["label"] for item in data]

    # Parâmetros
    vocab_size = 1000
    max_length = 100
    num_classes = len(set(labels))

    # Tokenização
    tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    X_train = pad_sequences(sequences, maxlen=max_length, padding='post')
    y_train = to_categorical(labels, num_classes=num_classes)

    # Cálculo dos pesos das classes
    class_weights = compute_class_weight('balanced', classes=np.unique(labels), y=labels)
    class_weight_dict = dict(enumerate(class_weights))

    # Modelo
    model = Sequential()
    model.add(Embedding(vocab_size, 64, input_length=max_length))
    model.add(LSTM(64, return_sequences=True))  # Adicionando LSTM
    model.add(GlobalAveragePooling1D())
    model.add(Dense(128, activation="relu"))  # Mais neurônios
    model.add(Dropout(0.5))  # Dropout de 50%
    model.add(Dense(num_classes, activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    model.fit(X_train, y_train, epochs=20, class_weight=class_weight_dict, verbose=1)

    # Salva o modelo
    os.makedirs("model", exist_ok=True)
    model.save(MODEL_PATH)

    # Salva o tokenizer
    with open(TOKENIZER_PATH, "wb") as f:
        pickle.dump(tokenizer, f)

    # Fazer previsões para avaliação
    y_pred = model.predict(X_train)
    y_pred = np.argmax(y_pred, axis=1)  # Converte as previsões em índices de classes
    y_true = np.argmax(y_train, axis=1)  # Converte as labels para índices

    # Gerar relatório de classificação
    print(classification_report(y_true, y_pred))
    predictions = model.predict(X_train[:10])  # Verificando as 10 primeiras previsões
    print(np.argmax(predictions, axis=1))  # Exibindo as previsões
    print(labels[:10])  # Comparando com os rótulos reais

    return {"message": "Modelo treinado e salvo com sucesso!"}