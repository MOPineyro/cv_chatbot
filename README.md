# CV Chatbot RAG

Un chatbot que utiliza Retrieval-Augmented Generation (RAG) para responder preguntas sobre CVs. El sistema permite cargar CVs en PDF y hacer consultas sobre la información contenida en ellos.

## Demo

[![CV Chatbot Demo](https://cdn.loom.com/sessions/thumbnails/4247e48a256940ab993778769ba2f649-with-play.gif)](https://www.loom.com/share/4247e48a256940ab993778769ba2f649?sid=be2e3857-6334-432b-94bb-64944c7395b1)

## Características

- Carga de CVs en formato PDF
- Procesamiento de texto usando LangChain
- Embeddings con OpenAI (text-embedding-3-small)
- Almacenamiento vectorial con Pinecone
- Generación de respuestas usando Mixtral 8x7B vía Groq
- Interfaz de usuario con Streamlit

## Requisitos

- Python 3.9+
- Cuenta de OpenAI (para embeddings)
- Cuenta de Pinecone (para almacenamiento vectorial)
- Cuenta de Groq (para LLM)

## Instalación

1. Clonar el repositorio
2. Configurar variables de entorno en `.env`

## Uso

1. Ejecutar el chatbot:

```bash
make run
```

2. Abrir el navegador en `http://localhost:8501`

3. Cargar CVs usando el panel lateral

4. Hacer preguntas sobre los CVs cargados

## Comandos Disponibles

- `make setup`: Instalar dependencias
- `make test`: Ejecutar pipeline de prueba
- `make run`: Iniciar aplicación Streamlit

## Tecnologías Utilizadas

- [LangChain](https://python.langchain.com/): Framework para aplicaciones LLM
- [OpenAI](https://openai.com/): Embeddings
- [Pinecone](https://www.pinecone.io/): Base de datos vectorial
- [Groq](https://groq.com/): LLM inference
- [Streamlit](https://streamlit.io/): Interfaz de usuario
