# CAPSTONE-PROJECT
ANÁLISIS DE SENTIMIENTOS EN LA COMUNIDAD DE TWITTER Y SU IMPACTO SOCIAL EN EL ACTUAR DE LA POBLACIÓN

Pasos para la instalación:
1. Crear un entorno virtual con la versión de python 3.10.11 (recomendación, usar anaconda o miniconda)
2. Tener instalado Jupyter Notebook en el entorno virtual creado.
3. Desde el cmd ubicado en el entorno virtual, instalar las siguientes librerías:
	-IBM-WATSON:
		pip install --upgrade ibm-watson
	-PANDAS:
		pip install pandas
	-OPENPYXL:
		pip install openpyxl
	-PYTHON-DOTENV:
		pip install python-dotenv
4. Crear un archivo .env con las variables de entorno, se recomienda usar la siguiente notación:
	-IBM_API_KEY=YOUR_APPI_KEY
	-IBM_URL_SERVICE=YOUR_URL

	-IMAGGA_API_KEY=YOUR_APPI_KEY_2
	-IMAGGA_API_SECRET=YOUR_API_SECRET

	-NLP_API_KEY=YOUR_APPI_KEY_3
	-NLP_API_HOST=YOUR_API_HOST
5. Realizar el clone

Objetivo: 
El objetivo de este proyecto es generar un análisis de sentimientos que considere el análisis de imágenes y textos 