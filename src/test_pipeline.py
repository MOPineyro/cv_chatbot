import os
from document_loader import DocumentLoader
from agents import AgentManager

def test_single_cv_queries():
    """Probar consultas individuales para cada CV"""
    print("\n=== Probando Consultas Individuales ===\n")
    
    # Inicializar componentes
    loader = DocumentLoader()
    agent_manager = AgentManager()
    
    # Cargar CVs
    cv_dir = "data/cvs"
    loaded_cvs = []
    
    for filename in os.listdir(cv_dir):
        if filename.endswith('.pdf'):
            print(f"\nCargando CV: {filename}")
            try:
                cv_path = os.path.join(cv_dir, filename)
                chunks = loader.load_pdf(cv_path)
                cv_text = " ".join(chunks)
                name = os.path.splitext(filename)[0]
                
                # Agregar agente para este CV
                agent_manager.add_agent(
                    name=name,
                    cv_text=cv_text,
                    is_default=(name.lower() == "manuel_pineyro")
                )
                loaded_cvs.append(name)
                print(f"✅ Cargado exitosamente")
            except Exception as e:
                print(f"❌ Error al cargar {filename}: {str(e)}")
    
    # Probar consultas para cada CV
    test_queries = [
        "Cuántos años de experiencia tiene {name}?",
        "En qué empresas trabajó {name}?",
        "Qué tecnologías domina {name}?",
        "Cuál es la formación académica de {name}?",
        "Qué roles ha tenido {name} en sus trabajos?"
    ]
    
    for name in loaded_cvs:
        print(f"\nProbando consultas para el CV de {name}:")
        for query_template in test_queries:
            query = query_template.format(name=name)
            print(f"\nConsulta: {query}")
            try:
                response = agent_manager.process_query(query)
                print(f"Respuesta: {response[:200]}...")
                print("✅ Consulta procesada exitosamente")
            except Exception as e:
                print(f"❌ Error procesando consulta: {str(e)}")

def test_default_agent():
    """Probar consultas sin especificar nombre (debe usar el CV de Manuel Pineyro)"""
    print("\n=== Probando Agente Predeterminado (Manuel Pineyro) ===\n")
    
    # Inicializar componentes
    loader = DocumentLoader()
    agent_manager = AgentManager()
    
    # Cargar CV de Manuel
    cv_path = os.path.join("data/cvs", "manuel_pineyro.pdf")
    if os.path.exists(cv_path):
        try:
            # Cargar y procesar el CV
            chunks = loader.load_pdf(cv_path)
            cv_text = " ".join(chunks)
            
            # Agregar agente y verificar que se estableció como predeterminado
            agent_manager.add_agent("manuel_pineyro", cv_text, is_default=True)
            
            if not agent_manager.default_agent:
                print("❌ Error: No se estableció el agente predeterminado")
                return
                
            # Verificar que el namespace es correcto
            print(f"Namespace del agente predeterminado: {agent_manager.default_agent.namespace}")
            
            # Verificar que hay contenido en el vector store
            context = agent_manager.default_agent.get_context("experiencia")
            if not context:
                print("❌ Error: No se encontró contenido en el vector store")
                return
            
            # Probar consultas predeterminadas
            test_queries = [
                "Cuántos años de experiencia tiene?",
                "En qué empresas has trabajado?",
                "Cuál es tu experiencia en desarrollo?",
                "Qué tecnologías conoces?",
                "Cuál es tu formación académica?",
                "Cuáles son tus roles más recientes?"
            ]
            
            for query in test_queries:
                print(f"\nConsulta (sin nombre): {query}")
                try:
                    response = agent_manager.process_query(query)
                    print(f"Respuesta: {response[:200]}...")
                    print("✅ Consulta procesada exitosamente")
                except Exception as e:
                    print(f"❌ Error procesando consulta: {str(e)}")
                    
        except Exception as e:
            print(f"❌ Error al cargar el CV de Manuel: {str(e)}")
    else:
        print("❌ No se encontró el CV de Manuel!")

def test_multi_cv_queries():
    """Probar consultas que involucran múltiples CVs"""
    print("\n=== Probando Consultas Multi-CV ===\n")
    
    # Inicializar componentes
    loader = DocumentLoader()
    agent_manager = AgentManager()
    
    # Cargar todos los CVs
    cv_dir = "data/cvs"
    for filename in os.listdir(cv_dir):
        if filename.endswith('.pdf'):
            try:
                cv_path = os.path.join(cv_dir, filename)
                chunks = loader.load_pdf(cv_path)
                cv_text = " ".join(chunks)
                name = os.path.splitext(filename)[0]
                agent_manager.add_agent(name, cv_text, is_default=(name.lower() == "manuel_pineyro"))
            except Exception as e:
                print(f"❌ Error al cargar {filename}: {str(e)}")
    
    # Probar consultas múltiples
    test_queries = [
        "Quién tiene más años de experiencia?",
        "Compara la experiencia en Python entre todos",
        "Quién tiene más experiencia en machine learning?",
        "Qué tecnologías tienen en común?",
        "Cuál es la formación académica de cada uno?",
        "Quién tiene experiencia en roles de liderazgo?"
    ]
    
    for query in test_queries:
        print(f"\nConsulta Multi-CV: {query}")
        try:
            response = agent_manager.process_query(query)
            print(f"Respuesta: {response[:200]}...")
            print("✅ Consulta procesada exitosamente")
        except Exception as e:
            print(f"❌ Error procesando consulta: {str(e)}")

def test_manuel_queries():
    print("\n=== Testing Manuel Pineyro Specific Queries ===\n")
    
    loader = DocumentLoader()
    agent_manager = AgentManager()
    
    cv_path = os.path.join("data/cvs", "manuel_pineyro.pdf")
    if os.path.exists(cv_path):
        try:
            chunks = loader.load_pdf(cv_path)
            cv_text = " ".join(chunks)
            agent_manager.add_agent("manuel_pineyro", cv_text, is_default=True)
            
            test_queries = [
                "Cuántos años de experiencia tiene Manuel Pineyro?",
                "En qué empresas trabajó Manuel?",
                "Qué experiencia tiene Pineyro en desarrollo?",
                "Cuál es la formación de Manuel Pineyro?",
                "Qué tecnologías domina Manuel?",
                "Cuáles son los últimos roles de Pineyro?"
            ]
            
            for query in test_queries:
                print(f"\nQuery: {query}")
                try:
                    response = agent_manager.process_query(query)
                    print(f"Response: {response[:200]}...")
                    print("✅ Query processed successfully")
                except Exception as e:
                    print(f"❌ Error processing query: {str(e)}")
        except Exception as e:
            print(f"❌ Error loading Manuel's CV: {str(e)}")
    else:
        print("❌ Manuel's CV not found!")

def test_language_handling():
    """Test responses in different languages"""
    print("\n=== Testing Language Handling ===\n")
    
    loader = DocumentLoader()
    agent_manager = AgentManager()
    
    cv_path = os.path.join("data/cvs", "manuel_pineyro.pdf")
    if os.path.exists(cv_path):
        try:
            chunks = loader.load_pdf(cv_path)
            cv_text = " ".join(chunks)
            agent_manager.add_agent("manuel_pineyro", cv_text, is_default=True)
            
            # Test queries in different languages
            test_queries = [
                # Spanish queries
                "Cuántos años de experiencia tiene Manuel Pineyro?",
                "Qué tecnologías domina?",
                # English queries
                "What is Manuel Pineyro's work experience?",
                "What technologies does he know?",
            ]
            
            for query in test_queries:
                print(f"\nQuery: {query}")
                try:
                    response = agent_manager.process_query(query)
                    print(f"Response: {response[:200]}...")
                    print("✅ Query processed successfully")
                except Exception as e:
                    print(f"❌ Error processing query: {str(e)}")
        except Exception as e:
            print(f"❌ Error loading Manuel's CV: {str(e)}")
    else:
        print("❌ Manuel's CV not found!")

if __name__ == "__main__":
    # # Test individual CV queries
    # test_single_cv_queries()
    
    # Test default agent (Manuel)
    test_default_agent()
    
    # # Test multi-CV queries
    # test_multi_cv_queries()
    
    # # Test Manuel Pineyro specific queries
    # test_manuel_queries()
    
    # # Test language handling
    # test_language_handling() 