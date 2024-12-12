from typing import Dict, Optional
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, LLM_MODEL_NAME

class NameExtractor:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=LLM_MODEL_NAME,
            temperature=0
        )
    
    def extract_name_from_cv(self, cv_text: str) -> Optional[str]:
        """Extraer el nombre completo del CV usando LLM"""
        prompt = """
        Por favor extrae el nombre completo de la persona de este CV.
        Responde SOLO con el nombre completo, sin texto adicional.
        Si no encuentras el nombre, responde 'DESCONOCIDO'.

        CV:
        {cv_text}
        """
        
        try:
            result = self.llm.predict(prompt.format(cv_text=cv_text[:1000]))
            return result.strip() if result.strip() != 'DESCONOCIDO' else None
        except Exception as e:
            print(f"Error extrayendo nombre: {str(e)}")
            return None 