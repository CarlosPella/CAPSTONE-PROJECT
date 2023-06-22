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
    tags = [tag['tag']['en'] for tag in json_data['result']['tags']]

    return tags

#FUNCION EXTRAER EMCIONES (IBM-WATSON API)
def extraer_emociones(texto):
    authenticator = IAMAuthenticator(os.environ.get('IBM_API_KEY'))
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(os.environ.get('IBM_URL_SERVICE'))
    
    response = natural_language_understanding.analyze(text=texto, features=Features(emotion=EmotionOptions())).get_result()
    result = json.dumps(response, indent=2)
    return json.loads(result)['emotion']['document']

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=r'recursos\Tweets.xlsx', help=r'Coloca la dirección del archivo de datos.Ejm:C:\Users\Ejemplo.xlsx')
    parser.add_argument('--columna_texto', type=str, default='text', help=r'Coloca el nombre de la columna donde se encuentra el texto del tweet')
    parser.add_argument('--columna_img', type=str, default='img_url', help=r'Coloca el nombre de la columna donde se encuentra la imagen del tweet')
    args = parser.parse_args()
    df = pd.read_excel(args.file);
    sys.stdout.write(str(df[args.columna_texto]))
    sys.stdout.write(str(df[args.columna_img]))


if __name__=='__main__':
    main()

#PRUEBAS
#COMENTAR=> CTRL K+CTRL C
#DESCOMENTAR=> CTRL K + CTRK U
#print(preprocesar_imagen('https://pbs.twimg.com/media/FzBxSvfaIAAdjyf?format=jpg&name=4096x4096'))
#print(extraer_emociones("@VirginAmerica and it's a really big bad thing about it"))
#print(calcular_ed(MATRIZ_PRUEBA,MATRIZ_EMOCIONES_PERFECTA))
# print(clasificar(1.1081969079,THRESHOLD))
#print(traducir_texto('Tome una piña colada y acabe ebrio'))

# matriz1 = [[1, 2, 3],
#            [4, 5, 6]]

# matriz2 = [[7, 8, 9],
#            [10, 11, 12]]

# print(promedio(matriz1,matriz2))


#prueba procesar imagen
# data2 = '{"result": {"tags": [{"confidence": 51.6775512695312, "tag": {"en": "hand"}}, {"confidence": 37.8711090087891, "tag": {"en": "technology"}}, {"confidence": 33.4202003479004, "tag": {"en": "business"}}, {"confidence": 33.1062202453613, "tag": {"en": "computer"}}, {"confidence": 32.4468803405762, "tag": {"en": "equipment"}}, {"confidence": 32.034065246582, "tag": {"en": "stereo"}}, {"confidence": 28.8875274658203, "tag": {"en": "device"}}, {"confidence": 25.4467754364014, "tag": {"en": "notebook"}}, {"confidence": 24.1064777374268, "tag": {"en": "office"}}, {"confidence": 23.8379878997803, "tag": {"en": "laptop"}}, {"confidence": 22.682991027832, "tag": {"en": "communication"}}, {"confidence": 21.9873161315918, "tag": {"en": "work"}}, {"confidence": 21.7257595062256, "tag": {"en": "hands"}}, {"confidence": 20.6586265563965, "tag": {"en": "keyboard"}}, {"confidence": 20.643533706665, "tag": {"en": "holding"}}, {"confidence": 20.257869720459, "tag": {"en": "person"}}, {"confidence": 20.0909461975098, "tag": {"en": "electronic equipment"}}, {"confidence": 18.8395977020264, "tag": {"en": "close"}}, {"confidence": 18.5690078735352, "tag": {"en": "working"}}, {"confidence": 18.4968128204346, "tag": {"en": "finger"}}, {"confidence": 18.2671566009521, "tag": {"en": "data"}}, {"confidence": 18.1970100402832, "tag": {"en": "closeup"}}, {"confidence": 17.7001953125, "tag": {"en": "job"}}, {"confidence": 17.4812908172607, "tag": {"en": "man"}}, {"confidence": 17.2987365722656, "tag": {"en": "people"}}, {"confidence": 17.2520484924316, "tag": {"en": "human"}}, {"confidence": 17.0262699127197, "tag": {"en": "digital"}}, {"confidence": 16.748836517334, "tag": {"en": "display"}}, {"confidence": 16.7356452941895, "tag": {"en": "button"}}, {"confidence": 16.6053485870361, "tag": {"en": "phone"}}, {"confidence": 16.1297168731689, "tag": {"en": "modern"}}, {"confidence": 16.1288051605225, "tag": {"en": "object"}}, {"confidence": 15.9467182159424, "tag": {"en": "information"}}, {"confidence": 15.7241897583008, "tag": {"en": "audio system"}}, {"confidence": 15.6126794815063, "tag": {"en": "male"}}, {"confidence": 15.1992874145508, "tag": {"en": "electronics"}}, {"confidence": 15.0900344848633, "tag": {"en": "mobile"}}, {"confidence": 14.3066720962524, "tag": {"en": "wireless"}}, {"confidence": 14.2893114089966, "tag": {"en": "fingers"}}, {"confidence": 14.0608501434326, "tag": {"en": "screen"}}, {"confidence": 14.0051050186157, "tag": {"en": "electronic"}}, {"confidence": 13.9006271362305, "tag": {"en": "telephone"}}, {"confidence": 13.7534980773926, "tag": {"en": "occupation"}}, {"confidence": 13.6163597106934, "tag": {"en": "headset"}}, {"confidence": 13.606707572937, "tag": {"en": "lens cap"}}, {"confidence": 13.5675811767578, "tag": {"en": "pen"}}, {"confidence": 12.802864074707, "tag": {"en": "connection"}}, {"confidence": 12.032865524292, "tag": {"en": "corporate"}}, {"confidence": 11.7651357650757, "tag": {"en": "paper"}}, {"confidence": 11.6679201126099, "tag": {"en": "keypad"}}, {"confidence": 11.5904140472412, "tag": {"en": "pointing"}}, {"confidence": 11.5016527175903, "tag": {"en": "key"}}, {"confidence": 11.4813652038574, "tag": {"en": "medical"}}, {"confidence": 11.4526062011719, "tag": {"en": "medicine"}}, {"confidence": 11.2603340148926, "tag": {"en": "education"}}, {"confidence": 11.076210975647, "tag": {"en": "hold"}}, {"confidence": 10.9870166778564, "tag": {"en": "finance"}}, {"confidence": 10.9497690200806, "tag": {"en": "cap"}}, {"confidence": 10.7215843200684, "tag": {"en": "typing"}}, {"confidence": 10.5984001159668, "tag": {"en": "businessman"}}, {"confidence": 10.1892833709717, "tag": {"en": "focus"}}, {"confidence": 9.91107082366943, "tag": {"en": "mouse"}}, {"confidence": 9.78568267822266, "tag": {"en": "input"}}, {"confidence": 9.71376800537109, "tag": {"en": "optical"}}, {"confidence": 9.5813045501709, "tag": {"en": "exam"}}, {"confidence": 9.40917110443115, "tag": {"en": "writing"}}, {"confidence": 9.28495979309082, "tag": {"en": "professional"}}, {"confidence": 9.24180793762207, "tag": {"en": "camera"}}, {"confidence": 9.2270336151123, "tag": {"en": "black"}}, {"confidence": 9.09132671356201, "tag": {"en": "portable computer"}}, {"confidence": 8.96193695068359, "tag": {"en": "one"}}, {"confidence": 8.66346549987793, "tag": {"en": "using"}}, {"confidence": 8.65343284606934, "tag": {"en": "desktop"}}, {"confidence": 8.646484375, "tag": {"en": "hardware"}}, {"confidence": 8.5729808807373, "tag": {"en": "blank"}}, {"confidence": 8.53096294403076, "tag": {"en": "tech"}}, {"confidence": 8.50521850585938, "tag": {"en": "desk"}}, {"confidence": 8.47559547424316, "tag": {"en": "web"}}, {"confidence": 8.46197319030762, "tag": {"en": "doctor"}}, {"confidence": 8.44306945800781, "tag": {"en": "showing"}}, {"confidence": 8.29538345336914, "tag": {"en": "executive"}}, {"confidence": 8.25630378723145, "tag": {"en": "letter"}}, {"confidence": 8.23325538635254, "tag": {"en": "care"}}, {"confidence": 8.22151756286621, "tag": {"en": "message"}}, {"confidence": 8.16385746002197, "tag": {"en": "protective covering"}}, {"confidence": 8.04883766174316, "tag": {"en": "success"}}, {"confidence": 8.02065467834473, "tag": {"en": "financial"}}, {"confidence": 7.99916696548462, "tag": {"en": "looking"}}, {"confidence": 7.96148109436035, "tag": {"en": "silver"}}, {"confidence": 7.85848140716553, "tag": {"en": "instrument"}}, {"confidence": 7.8117823600769, "tag": {"en": "modem"}}, {"confidence": 7.80132246017456, "tag": {"en": "beautician"}}, {"confidence": 7.79285335540771, "tag": {"en": "table"}}, {"confidence": 7.78887939453125, "tag": {"en": "paperwork"}}, {"confidence": 7.69053220748901, "tag": {"en": "monitor"}}, {"confidence": 7.65975332260132, "tag": {"en": "tool"}}, {"confidence": 7.64920282363892, "tag": {"en": "communicate"}}, {"confidence": 7.64507579803467, "tag": {"en": "health"}}, {"confidence": 7.62632656097412, "tag": {"en": "workplace"}}, {"confidence": 7.56541872024536, "tag": {"en": "plan"}}, {"confidence": 7.52481746673584, "tag": {"en": "hospital"}}, {"confidence": 7.42589855194092, "tag": {"en": "document"}}, {"confidence": 7.41867208480835, "tag": {"en": "show"}}, {"confidence": 7.41198253631592, "tag": {"en": "indoors"}}, {"confidence": 7.39009666442871, "tag": {"en": "teamwork"}}, {"confidence": 7.33776092529297, "tag": {"en": "holding hands"}}, {"confidence": 7.33197736740112, "tag": {"en": "map"}}, {"confidence": 7.27520513534546, "tag": {"en": "equipment"}}, {"confidence": 7.24266004562378, "tag": {"en": "metal"}}, {"confidence": 7.23962163925171, "tag": {"en": "talking"}}, {"confidence": 7.19385004043579, "tag": {"en": "collaboration"}}, {"confidence": 7.16980266571045, "tag": {"en": "close-up"}}, {"confidence": 7.15705156326294, "tag": {"en": "corporate executive"}}, {"confidence": 7.13873338794708, "tag": {"en": "book"}}, {"confidence": 7.1279673576355, "tag": {"en": "using phone"}}, {"confidence": 7.11296463012695, "tag": {"en": "blue"}}, {"confidence": 7.10129690170288, "tag": {"en": "sitting"}}, {"confidence": 7.07827615737915, "tag": {"en": "administrator"}}, {"confidence": 7.06641912460327, "tag": {"en": "machine"}}, {"confidence": 7.06137418746948, "tag": {"en": "plant"}}, {"confidence": 7.02724552154541, "tag": {"en": "close up"}}, {"confidence": 7.02037143707275, "tag": {"en": "director"}}, {"confidence": 6.97738885879517, "tag": {"en": "city"}}, {"confidence": 6.96209144592285, "tag": {"en": "smartphone"}}, {"confidence": 6.95443677902222, "tag": {"en": "female"}}, {"confidence": 6.93846416473389, "tag": {"en": "silver-colored"}}, {"confidence": 6.92164659500122, "tag": {"en": "clinic"}}, {"confidence": 6.88961124420166, "tag": {"en": "pad"}}, {"confidence": 6.88510751724243, "tag": {"en": "research"}}, {"confidence": 6.86276054382324, "tag": {"en": "team"}}, {"confidence": 6.85269260406494, "tag": {"en": "medical professional"}}, {"confidence": 6.83472585678101, "tag": {"en": "pen"}}, {"confidence": 6.8250846862793, "tag": {"en": "tablet computer"}}, {"confidence": 6.79131412506104, "tag": {"en": "note pad"}}, {"confidence": 6.78915691375732, "tag": {"en": "internet"}}]}, "success": true}'
# print(preprocesar_imagen(data2))

