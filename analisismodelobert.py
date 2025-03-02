# -*- coding: utf-8 -*-
"""AnalisisModeloBERT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m9cCxhnCu4Dj6A696Yvqm3nIUZOSnc-M
"""

!pip install transformers torch pandas matplotlib
!pip install wordcloud
from wordcloud import WordCloud

import torch
import pandas as pd
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Modelo de BETO para análisis de sentimientos en español
modelo = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(modelo)
modelo_beto = AutoModelForSequenceClassification.from_pretrained(modelo)

def analizar_sentimiento(texto):
    # Tokenizar el texto para que el modelo lo entienda
    inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Realizar la predicción sin actualizar pesos (no entrenamos, solo inferimos)
    with torch.no_grad():
        outputs = modelo_beto(**inputs)

    logits = outputs.logits
    prediccion = torch.argmax(logits, dim=1).item()

    # Mapear la predicción a etiquetas de sentimiento
    etiquetas = {
        0: "Muy negativo",
        1: "Negativo",
        2: "Neutral",
        3: "Positivo",
        4: "Muy positivo"
    }

    return etiquetas.get(prediccion, "Desconocido")

#load file and extract keys from twitter
from google.colab import files
uploaded = files.upload()

#Get the data from the file
#store the csv file to some variable
df = pd.read_csv('sentiment_data.csv')
print(df.head())

# Seleccionar solo la columna de texto y eliminar filas vacías
df = df[['texto']].dropna()

import re
import unicodedata

def clean_text(text):
    text = str(text)  # Asegurar que sea string
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Eliminar menciones
    text = re.sub(r'#', '', text)  # Eliminar hashtags
    text = re.sub(r'RT[\s]+', '', text)  # Eliminar RT
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Eliminar URLs
    text = re.sub(r'[^\w\s]', '', text)  # Eliminar signos de puntuación
    text = text.lower()  # Convertir a minúsculas
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')  # Quitar acentos
    return text

# Aplicar limpieza
df['Cleaned_Text'] = df['texto'].apply(clean_text)

!pip install swifter

import swifter
df['Sentimiento'] = df['Cleaned_Text'].swifter.apply(analizar_sentimiento)

# Contar cuántos comentarios de cada tipo hay
sentiment_counts = df['Sentimiento'].value_counts()

# Graficar distribución de análisis de sentimientos
sentiment_counts.plot(kind='bar', color=['red', 'orange', 'gray', 'lightblue', 'green'])
plt.title('Distribución de Sentimientos en Redes Sociales')
plt.xlabel('Sentimiento')
plt.ylabel('Cantidad')
plt.show()

# Generar una nube de palabras
all_words = ' '.join([text for text in df['Cleaned_Text']])
wordcloud = WordCloud(width=800, height=500, max_font_size=110, background_color='white').generate(all_words)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()