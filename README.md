# CV Chatbot

[English](#english) | [Español](#español)

# English

An agent-based Retrieval-Augmented Generation (RAG) chatbot for CV/resume analysis. The system uses specialized agents to handle different CVs, enabling both individual and comparative analysis through natural language queries.

## Demo

- [Watch Demo Video](https://www.loom.com/share/36b26fac33e44da288ba191d8f092db6?sid=90de9f94-2591-4b26-8336-f79b8f254693)

## Features

- **Agent-Based Architecture**:

  - Individual agents for each CV
  - Intelligent query routing
  - Multi-CV comparison capabilities
  - Default agent for general queries

- **Advanced RAG Implementation**:

  - PDF CV/resume processing
  - Semantic chunking and embedding
  - Context-aware retrieval
  - Bilingual support (English/Spanish)

## Technologies Used

- [LangChain](https://python.langchain.com/): LLM application framework
- [OpenAI](https://openai.com/): Text embeddings (text-embedding-3-small)
- [Pinecone](https://www.pinecone.io/): Vector database
- [Groq](https://groq.com/): LLM inference (Mixtral 8x7B)
- [Streamlit](https://streamlit.io/): User interface

## Requirements

- Python 3.9+
- OpenAI account (embeddings)
- Pinecone account (vector storage)
- Groq account (LLM)

## Installation

1. Clone the repository
2. Configure environment variables in `.env`:

```bash
OPENAI_API_KEY=your_key
PINECONE_API_KEY=your_key
GROQ_API_KEY=your_key
PINECONE_INDEX_NAME=your_index
```

## Usage

1. Start the application:

```bash
make run
```

2. Open `http://localhost:8501`

3. Upload CVs through the sidebar

4. Query types:
   - Individual CV: "What is Ana's experience with Python?"
   - Default agent: "Tell me about your education"
   - Multi-CV comparison: "Who has more experience in machine learning?"

## Commands

- `make setup`: Install dependencies
- `make test`: Run test pipeline
- `make test-names`: Test name extraction
- `make run`: Launch Streamlit app

## Architecture

- `agents.py`: Agent management and query processing
- `vector_store.py`: Embedding and retrieval logic
- `language_detector.py`: Language detection
- `name_extractor.py`: Name extraction from CVs and queries

---

# Español

Un chatbot basado en agentes que utiliza Retrieval-Augmented Generation (RAG) para análisis de CVs. El sistema emplea agentes especializados para manejar diferentes CVs, permitiendo tanto análisis individual como comparativo mediante consultas en lenguaje natural.

## Demo

- [Ver Video Demo](https://www.loom.com/share/36b26fac33e44da288ba191d8f092db6?sid=90de9f94-2591-4b26-8336-f79b8f254693)

## Características

- **Arquitectura Basada en Agentes**:

  - Agentes individuales para cada CV
  - Enrutamiento inteligente de consultas
  - Capacidad de comparación multi-CV
  - Agente predeterminado para consultas generales

- **Implementación RAG Avanzada**:

  - Procesamiento de CVs en PDF
  - Segmentación y embedding semántico
  - Recuperación contextual
  - Soporte bilingüe (Español/Inglés)

## Tecnologías Utilizadas

- [LangChain](https://python.langchain.com/): Framework para aplicaciones LLM
- [OpenAI](https://openai.com/): Embeddings (text-embedding-3-small)
- [Pinecone](https://www.pinecone.io/): Base de datos vectorial
- [Groq](https://groq.com/): LLM inference (Mixtral 8x7B)
- [Streamlit](https://streamlit.io/): Interfaz

## Requisitos

- Python 3.9+
- Cuenta OpenAI (embeddings)
- Cuenta Pinecone (almacenamiento vectorial)
- Cuenta Groq (LLM)

## Instalación

1. Clonar el repositorio
2. Configurar variables de entorno en `.env`:

```bash
OPENAI_API_KEY=tu_clave
PINECONE_API_KEY=tu_clave
GROQ_API_KEY=tu_clave
PINECONE_INDEX_NAME=tu_indice
```

## Uso

1. Iniciar la aplicación:

```bash
make run
```

2. Abrir `http://localhost:8501`

3. Cargar CVs a través del panel lateral

4. Tipos de consultas:
   - CV individual: "Qué experiencia tiene Ana en Python?"
   - Agente predeterminado: "Cuéntame sobre tu educación"
   - Comparación multi-CV: "Quién tiene más experiencia en machine learning?"

## Comandos

- `make setup`: Instalar dependencias
- `make test`: Ejecutar pipeline de pruebas
- `make test-names`: Probar extracción de nombres
- `make run`: Iniciar app Streamlit

## Arquitectura

- `agents.py`: Gestión de agentes y procesamiento de consultas
- `vector_store.py`: Lógica de embeddings y recuperación
- `language_detector.py`: Detección de idioma
- `name_extractor.py`: Extracción de nombres de CVs y consultas
