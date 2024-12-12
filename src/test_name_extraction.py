import os
from name_extractor import NameExtractor
from document_loader import DocumentLoader

def test_name_extraction():
    """Test the name extraction functionality"""
    
    # Initialize components
    extractor = NameExtractor()
    loader = DocumentLoader()
    
    # Test directory
    cv_dir = "data/cvs"
    if not os.path.exists(cv_dir):
        print(f"Error: Directory {cv_dir} not found!")
        return
    
    print("\n=== Testing Name Extraction ===\n")
    
    # Test each CV in the directory
    for filename in os.listdir(cv_dir):
        if filename.endswith('.pdf'):
            print(f"\nTesting CV: {filename}")
            try:
                # Load CV
                cv_path = os.path.join(cv_dir, filename)
                chunks = loader.load_pdf(cv_path)
                cv_text = " ".join(chunks)
                
                # Extract name
                extracted_name = extractor.extract_name_from_cv(cv_text)
                
                # Get expected name from filename
                expected_name = os.path.splitext(filename)[0]
                
                # Print results
                print(f"Expected name (from filename): {expected_name}")
                print(f"Extracted name: {extracted_name or 'NONE'}")
                
                if extracted_name:
                    print("✅ Name extracted successfully")
                else:
                    print("❌ Failed to extract name")
                
            except Exception as e:
                print(f"❌ Error processing {filename}: {str(e)}")

def test_name_detection_in_queries():
    """Test the name detection in various types of queries"""
    
    # Sample CV text for testing
    sample_cv = """
    CURRICULUM VITAE
    
    Nombre: Manuel Pérez González
    Email: manuel.perez@email.com
    
    Experiencia...
    """
    
    # Initialize components
    from agents import AgentManager
    
    agent_manager = AgentManager()
    agent_manager.add_agent("manuel", sample_cv, is_default=True)
    
    # Test queries
    test_queries = [
        "Cuál es la experiencia de Manuel?",
        "Háblame sobre Manuel Pérez",
        "Qué estudió Manuel Pérez González?",
        "Cuáles son sus habilidades?",  # No name mentioned
        "Dónde trabajó Pérez?",
        "González tiene experiencia en Python?",
    ]
    
    print("\n=== Testing Name Detection in Queries ===\n")
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        names = agent_manager.extract_names(query)
        print(f"Detected names: {names}")
        if names:
            print("✅ Names detected")
        else:
            print("ℹ️ No names detected")

if __name__ == "__main__":
    # Test name extraction from CVs
    test_name_extraction()
    
    # Test name detection in queries
    test_name_detection_in_queries() 