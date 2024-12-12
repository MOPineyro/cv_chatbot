# CV Chatbot RAG

[English](#english) | [Español](#español)

# English

A chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions about CVs/resumes. The system allows uploading PDFs and querying information contained within them.

## Demo

- [Watch Demo Video](https://www.loom.com/share/4247e48a256940ab993778769ba2f649?sid=be2e3857-6334-432b-94bb-64944c7395b1)

## Features

- PDF CV/resume upload
- Text processing using LangChain
- Embeddings with OpenAI (text-embedding-3-small)
- Vector storage with Pinecone
- Response generation using Mixtral 8x7B via Groq
- Streamlit user interface

## Requirements

- Python 3.9+
- OpenAI account (for embeddings)
- Pinecone account (for vector storage)
- Groq account (for LLM)

## Installation

1. Clone the repository
2. Configure environment variables in `.env`

## Usage

1. Run the chatbot:

```bash
make run
```

2. Open browser at `http://localhost:8501`

3. Upload CVs using the sidebar

4. Ask questions about the loaded CVs

## Available Commands

- `make setup`: Install dependencies
- `make test`: Run test pipeline
- `make run`: Start Streamlit application

## Technologies Used

- [LangChain](https://python.langchain.com/): Framework for LLM applications
- [OpenAI](https://openai.com/): Embeddings
- [Pinecone](https://www.pinecone.io/): Vector database
- [Groq](https://groq.com/): LLM inference
- [Streamlit](https://streamlit.io/): User interface

---

# Español

Un chatbot que utiliza Retrieval-Augmented Generation (RAG) para responder preguntas sobre CVs. El sistema permite cargar CVs en PDF y hacer consultas sobre la información contenida en ellos.

## Demo

- [Ver Video Demo](https://www.loom.com/share/4247e48a256940ab993778769ba2f649?sid=be2e3857-6334-432b-94bb-64944c7395b1)

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
