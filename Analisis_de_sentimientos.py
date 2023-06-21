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

#DATOS PREDEFINIDOS
load_dotenv()
THRESHOLD = 1.083274218344552
MATRIZ_EMOCIONES_PERFECTA = '{ "emotion": {"sadness" : 0.005441, "joy" : 0.997533, "fear" : 0.009288, "disgust" : 0.001843, "anger" : 0.002108}}'
MATRIZ_PRUEBA = '{ "emotion": {"sadness" : 0.523502, "joy" : 0.060197, "fear" : 0.034915, "disgust" : 0.124649, "anger" : 0.257796}}'

0.05441 + 0.523502
#CREACIÓN DE FUNCIONES
#FUNCION PRE-PROCESAR IMAGEN
def preprocesar_imagen(url):
    response = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % url,
                            auth=(os.environ.get('IMAGGA_API_KEY'), os.environ.get('IMAGGA_API_SECRET')))
    return response.json()

#FUNCION EXTRAER EMCIONES (IBM-WATSON API)
def extraer_emociones(texto):
    authenticator = IAMAuthenticator(os.environ.get('IBM_API_KEY'))
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(os.environ.get('IBM_URL_SERVICE'))
    
    response = natural_language_understanding.analyze(text=texto, features=Features(emotion=EmotionOptions())).get_result()
    return json.dumps(response, indent=2)

#FUNCION CALCULAR VALOR ED
def calcular_ed(json1,json2):
    data1 = json.loads(json1)
    data2 = json.loads(json2)

    x = list(data1['emotion'].values())
    y = list(data2['emotion'].values())
    print(x)

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

#FUNCION PROMEDIO ENTRE 2 JSON
def prom(json1,json2):
    data1 = json.loads(json1)
    data2 = json.loads(json2)

    x = list(data1['emotion'].values())
    y = list(data2['emotion'].values())
    
    if len(x) != len(y):
        raise ValueError("Las matrices deben tener la misma cantidad de valores")

    resultado = [(xi + yi) / 2 for xi, yi in zip(x, y)]

    return resultado

#PRUEBAS
#COMENTAR=> CTRL K+CTRL C
#DESCOMENTAR=> CTRL K + CTRK U
# print(preprocesar_imagen('https://pbs.twimg.com/media/FzBxSvfaIAAdjyf?format=jpg&name=4096x4096'))
# print(extraer_emociones("@VirginAmerica and it's a really big bad thing about it"))
#print(calcular_ed(MATRIZ_PRUEBA,MATRIZ_EMOCIONES_PERFECTA))
# print(clasificar(1.1081969079,THRESHOLD))
#print(traducir_texto('Tome una piña colada y acabe ebrio'))

# matriz1 = [[1, 2, 3],
#            [4, 5, 6]]

# matriz2 = [[7, 8, 9],
#            [10, 11, 12]]

# print(promedio(matriz1,matriz2))