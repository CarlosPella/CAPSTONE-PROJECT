#Importamos las librerías necesarias
from dotenv import load_dotenv
import os
import json
import requests
import pandas as pd
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
import Features, EmotionOptions
from functools import reduce
from math import sqrt
import argparse
import sys
from langdetect import detect
import re

#DATOS PREDEFINIDOS
load_dotenv()
THRESHOLD = 1.083274218344552
MATRIZ_EMOCIONES_PERFECTA = '{ "emotion": {"sadness" : 0.005441, "joy" : 0.997533, "fear" : 0.009288, "disgust" : 0.001843, "anger" : 0.002108}}'
MATRIZ_PRUEBA = '{ "emotion": {"sadness" : 0.523502, "joy" : 0.060197, "fear" : 0.034915, "disgust" : 0.124649, "anger" : 0.257796}}'

#CREACIÓN DE FUNCIONES

#FUNCION PRE-PROCESAR IMAGEN
def preprocesar_imagen(url):
    params = {
        'image_url': url,
        'threshold': 20
    }
    response = requests.get(
        'https://api.imagga.com/v2/tags',
        params=params,
        auth=(os.environ.get('IMAGGA_API_KEY'), os.environ.get('IMAGGA_API_SECRET'))
    )
    
    json_data = response.json()
    tags = ' '.join(tag['tag']['en'] for tag in json_data['result']['tags'])

    return tags

#FUNCION EXTRAER EMCIONES (IBM-WATSON API)
def extraer_emociones(texto):
    authenticator = IAMAuthenticator(os.environ.get('IBM_API_KEY'))
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(os.environ.get('IBM_URL_SERVICE'))
    
    response = natural_language_understanding.analyze(text=texto, features=Features(emotion=EmotionOptions())).get_result()
    result = json.dumps(response, indent=2)
    data = json.loads(result)['emotion']['document']
    return list(data['emotion'].values())

#FUNCION CALCULAR VALOR ED
def calcular_ed(matriz1,matriz2):
    x = matriz1
    y = matriz2

    if len(x) != len(y):
        raise ValueError("Las matrices deben tener la misma longitud")

    resultado = reduce(lambda a, b: a + b, [(yi - xi)**2 for xi, yi in zip(x, y)])
    return sqrt(resultado)

#FUNCION CLASIFICAR (POSITIVO O NEGATIVO)
def clasificar(ed,threshold):
    return 'positivo' if ed < threshold else 'negativo'

#FUNCION TRADUCCIR (NLP API)
def traducir_texto(text):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"

    headers ={
        "X-RapidAPI-Key": os.environ.get('NLP_API_KEY'),
        "X-RapidAPI-Host": os.environ.get('NLP_API_HOST')
    }
    querystring = {"text": text, "to": "en"}
    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()

    if response.status_code == 200:
        trad = response_data['translated_text']['en']
        return trad
    else:
        return None

#FUNCION PROMEDIO ENTRE 2 matrices
def prom(x,y):
    if len(x) != len(y):
        raise ValueError("Las matrices deben tener la misma cantidad de valores")

    resultado = [(xi + yi) / 2 for xi, yi in zip(x, y)]

    return resultado

def hay_valor(cell):
    return pd.notnull(cell)

def detectar_idioma(text):
    idioma = detect(text)
    return idioma


def eliminar_caracteres_especiales(texto):
    # Expresión regular para encontrar caracteres especiales excepto los acentuados en inglés
    patron = r'[^a-zA-Z0-9@:;\-\'\s]'
    
    # Reemplazar caracteres especiales con una cadena vacía
    resultado = re.sub(patron, '', texto)
    
    return resultado


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=r'recursos\Tweets.xlsx', help=r'Coloca la dirección del archivo de datos.Ejm:C:\Users\Ejemplo.xlsx')
    parser.add_argument('--columna_texto', type=str, default='text', help=r'Coloca el nombre de la columna donde se encuentra el texto del tweet')
    parser.add_argument('--columna_img', type=str, default='img_url', help=r'Coloca el nombre de la columna donde se encuentra la imagen del tweet')
    args = parser.parse_args()
    df = pd.read_excel(args.file, usecols=[args.columna_texto,args.columna_img]);
    lista = df.to_numpy().tolist()
    to_excel = []
    for row in lista:
        text = False
        img_text = False
        emotions_text = False
        emotions_img = False

        if hay_valor(row[0]):
            text = eliminar_caracteres_especiales(row[0])
            texto_trad = text
            if detectar_idioma(text)!='en':
                texto_trad = traducir_texto(text)
            emotions_text = extraer_emociones(texto_trad)

        if hay_valor(row[1]):
            img_text = preprocesar_imagen(row[1])
            emotions_img = extraer_emociones(img_text)

        matriz_resultante = emotions_text
        if emotions_text != False and emotions_img != False:
            matriz_resultante = prom(emotions_text,emotions_img)

        matriz_emociones_perfecta = json.loads(MATRIZ_EMOCIONES_PERFECTA)
        lista_emociones_pefecta = list(matriz_emociones_perfecta['emotion'].values())
        
        ed = calcular_ed(matriz_resultante,lista_emociones_pefecta)
        
        clasificador = clasificar(ed,THRESHOLD)
        row.append(matriz_resultante)
        row.append(ed)
        row.append(clasificador)
        to_excel.append(row)
    
    headers = ['texto', 'imagen_url', 'array emociones', 'ed', 'clasificador']

    df = pd.DataFrame(to_excel, columns=headers)
    df.to_excel(r'recursos\output.xlsx', index=False)

if __name__=='__main__':
    main()