from document_loader import DocumentLoader
from vector_store import VectorStore

def format_result(result):
    """Format the result to show relevant information."""
    # Extract name from the text
    if "Ana García" in result['text']:
        name = "Ana García"
    elif "Carlos Rodríguez" in result['text']:
        name = "Carlos Rodríguez"
    else:
        name = "Desconocido"
    
    return f"\n{name} (Score: {result['score']:.4f}):\n{'-' * 40}\n{result['text']}\n"

def test_pipeline():
    try:
        # Inicializar componentes
        loader = DocumentLoader()
        vector_store = VectorStore()
        
        # Cargar los PDFs
        cvs = ['data/cvs/sample_ana.pdf', 'data/cvs/sample_carlos.pdf']
        all_chunks = []
        
        for cv_path in cvs:
            chunks = loader.load_pdf(cv_path)
            print(f"\nSe cargaron {len(chunks)} fragmentos de {cv_path}")
            all_chunks.extend(chunks)
        
        # Agregar todos los fragmentos al almacén vectorial
        ids = vector_store.add_texts(all_chunks)
        print(f"\nSe agregaron {len(ids)} vectores a Pinecone")
        
        # Consultas específicas para probar el sistema
        queries = [
            "¿Quién tiene experiencia en Python?",
            "¿Quién tiene experiencia en machine learning?",
            "¿Cuál es la experiencia de Ana en desarrollo web?",
            "¿Qué estudió Carlos y cuál fue su promedio?",
            "¿Quién tiene experiencia con bases de datos?",
            "¿Qué tecnologías cloud manejan los candidatos?",
            "¿Cuál es la experiencia en liderazgo de equipos?"
        ]

        for query in queries:
            print(f"\n\n{'=' * 50}")
            print(f"Consulta: {query}")
            print('=' * 50)
            results = vector_store.similarity_search(query, k=2)
            
            if results:
                for result in results:
                    print(format_result(result))
            else:
                print("\nNo se encontraron resultados.")
        
    except Exception as e:
        print(f"Error en el pipeline de prueba: {str(e)}")

if __name__ == "__main__":
    test_pipeline() 