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

