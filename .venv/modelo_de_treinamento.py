import pandas as pd
import json
import csv
import time
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words_pt = stopwords.words('portuguese')

def treinar_modelo_sentimento():
    #função que vai treinar a rede neural e retorna os dados necessários para a interface gráfica
    try:
        with open('classified_articles_rotulado.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        df = pd.DataFrame(dados)
        X = df['content']
        y = df['sentiment']

        vectorizer = TfidfVectorizer(stop_words=stop_words_pt, max_features=5000)
        X_vetorizado = vectorizer.fit_transform(X).toarray()

        # Transforma rótulos (Categorias para Números)
        label_encoder = LabelEncoder()
        y_enc = label_encoder.fit_transform(y)
        y_final = tf.keras.utils.to_categorical(y_enc)

        # Divisão Treino/Teste (80% treino, 20% teste)
        X_treino, X_teste, y_treino, y_teste = train_test_split(
            X_vetorizado, y_final, test_size=0.2, random_state=42
        )

        # Criação da Rede Neural Profunda
        model_mlp_sentimento = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=10000)

        print("-" * 50)
        print("INICIANDO TREINAMENTO")
        print("-" * 50)

        inicio_tempo = time.time()

        model_mlp_sentimento.fit(X_treino, y_treino)

        fim_tempo = time.time()
        print("-" * 50)

        y_predicted = model_mlp_sentimento.predict(X_teste)
        acuracia = accuracy_score(y_teste, y_predicted)
        tempo_total = fim_tempo - inicio_tempo

        print(acuracia)

        return model_mlp_sentimento, vectorizer, acuracia, tempo_total, label_encoder

    except FileNotFoundError:
        print("Erro: Arquivo 'classified_articles_rotulado.json' não encontrado!")
        return None, None, 0, 0, None

def treinar_modelo_topic():
    #função que vai treinar a rede neural e retorna os dados necessários para a interface gráfica
    try:
        with open('classified_articles_rotulado.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        df = pd.DataFrame(dados)
        X = df['content']
        y = df['topic']

        vectorizer2 = TfidfVectorizer(stop_words=stop_words_pt, max_features=5000)
        X_vetorizado = vectorizer2.fit_transform(X).toarray()

        # Transforma rótulos (Categorias para Números)
        label_encoder2 = LabelEncoder()
        y_enc = label_encoder2.fit_transform(y)
        y_final = tf.keras.utils.to_categorical(y_enc)

        # Divisão Treino/Teste (80% treino, 20% teste)
        X_treino, X_teste, y_treino, y_teste = train_test_split(
            X_vetorizado, y_final, test_size=0.2, random_state=42
        )

        # Criação da Rede Neural Profunda
        model_arvore_topico = tree.DecisionTreeClassifier()

        print("-" * 50)
        print("INICIANDO TREINAMENTO")
        print("-" * 50)

        inicio_tempo = time.time()

        model_arvore_topico.fit(X_treino, y_treino)

        fim_tempo = time.time()
        print("-" * 50)

        y_predicted = model_arvore_topico.predict(X_teste)
        acuracia2 = accuracy_score(y_teste, y_predicted)
        tempo_total2 = fim_tempo - inicio_tempo

        print(acuracia2)

        return model_arvore_topico, vectorizer2, acuracia2, tempo_total2, label_encoder2

    except FileNotFoundError:
        print("Erro: Arquivo 'classified_articles_rotulado.json' não encontrado!")
        return None, None, 0, 0, None

def obter_dataframe_completo():
 # Função principal para a interface realizar cálculos e gerar gráficos
    try:
        dados = pd.read_csv('dados_tabelados.csv')
        return pd.DataFrame(dados)
    except FileNotFoundError:
        return pd.DataFrame()