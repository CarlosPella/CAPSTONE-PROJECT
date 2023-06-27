# CAPSTONE-PROJECT
ANÁLISIS DE SENTIMIENTOS EN LA COMUNIDAD DE TWITTER Y SU IMPACTO SOCIAL EN EL ACTUAR DE LA POBLACIÓN

Pasos para la instalación:
1. Tener instalado un editor de código preferiblemente VSCODE
2. Descargar Anaconda o miniconda
3. Generar las credenciales de las siguientes APIS
	- IMAGGA
	- NLP
	- IBM-CLOUD
4. Crear entorno virtual en la versión Python 3.10.11
5. Entrar al entorno virtual
6. Instalaciones desde el prompt
  - IBM-WATSON: 
	- pip install --upgrade ibm-watson 
  - PANDAS: 
	- pip install pandas 
  - OPENPYXL: 
	- pip install openpyxl
  - PYTHON-DOTENV: 
	- pip install python-dotenv 
  - LANGDETECT
	- pip install langdetect
7. Realizar el clone del repositiorio desde github: https://github.com/CarlosPella/CAPSTONE-PROJECT.git
8. Modificar el archivo .env para las credenciales
	(Recomendación, seguir la siguiente notación)
	- IBM_API_KEY=YOUR_APPI_KEY 
	- IBM_URL_SERVICE=YOUR_API_URL
	- IMAGGA_API_KEY=YOUR_APPI_KEY_2 
	- IMAGGA_API_SECRET=YOUR_API_SECRET
	- NLP_API_KEY=YOUR_APPI_KEY_3
	- NLP_API_HOST=YOUR_API_HOST

# Objetivo: 
El objetivo de este proyecto es generar un análisis de sentimientos que considere el análisis de imágenes y textos, logrando así mejorar la precisión del modelo al poder contar con un contexto más claro de lo que los usuarios buscan expresar. 

# Entradas:
Para la correcta funcionalidad de nuestro prototipo, es necesario que se cuente con un dataset en excel con una columna que contenga textos (referenciando los posts que se van a analizar) y una columna que contenga los URL de las imagenes que contenia dicho post. 

# Salidas:
Nuestro prototipo brinda las siguientes salidas al usuario, devuelve un archivo excel denominado por defecto output con las siguientes columnas:
- Columna Texto: Texto analizado
- Columna IMG_URL: Url de las imágenes analizadas
- Array de emociones: Array de emociones obtenido por el análisis en conjunto de texto e imágen
- Columna ED Total: Valor ED obtenido por el análisis en conjunto de texto e imágen.
- Columna Clasificador Total: Clasificación del post (texto e imágen) en positivo y negativo.
- Columna ED (Solo Texto): Valor ED obtenido por el análisis de solo texto.
- Clasificador (Solo Texto): Clasificación del post (solo texto) en positivo y negativo.
