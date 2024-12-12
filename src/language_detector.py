from langdetect import detect, DetectorFactory
from typing import Optional

DetectorFactory.seed = 0

class LanguageDetector:
    LANGUAGE_MARKERS = {
        'es': {
            'question_words': ['qué', 'cuál', 'cómo', 'dónde', 'quién', 'cuándo', 'cuánto', 'por qué'],
            'markers': ['el', 'la', 'los', 'las', 'es', 'son', 'está', 'tienen', 'tiene'],
            'punctuation': ['¿', '¡']
        },
        'en': {
            'question_words': ['what', 'which', 'how', 'where', 'who', 'when', 'why', 'whose'],
            'markers': ['the', 'is', 'are', 'has', 'have', 'does', 'do'],
            'punctuation': ['?', '!']
        }
    }

    @classmethod
    def detect_language(cls, text: str) -> str:
        """
        Detect the language of the text using multiple methods
        Returns: 'es' for Spanish, 'en' for English
        """
        text = text.lower().strip()
        
        # Method 1: Check for distinctive punctuation
        if '¿' in text or '¡' in text:
            return 'es'
            
        # Method 2: Check for language-specific markers
        words = text.split()
        
        # Count markers for each language
        scores = {'es': 0, 'en': 0}
        
        for lang, markers in cls.LANGUAGE_MARKERS.items():
            # Check question words
            if any(word in text for word in markers['question_words']):
                scores[lang] += 2
            
            # Check other markers
            for marker in markers['markers']:
                if marker in words:
                    scores[lang] += 1
        
        # Method 3: Use langdetect as backup
        try:
            detected = detect(text)
            if detected in ['es', 'en']:
                scores[detected] += 3
        except:
            pass
        
        # Return the language with highest score, default to English if tied
        return 'es' if scores['es'] > scores['en'] else 'en'

    @classmethod
    def get_response_template(cls, detected_lang: str, is_default_agent: bool = False) -> dict:
        """
        Get the appropriate template based on language
        """
        if is_default_agent:
            templates = {
                'es': {
                    'template': """Eres un asistente experto analizando el CV de Manuel Pineyro.
                    
                    El CV contiene la siguiente información:
                    {context}
                    
                    Pregunta: {query}
                    
                    Proporciona una respuesta detallada y objetiva en español, basada en el CV.
                    Evita usar primera persona. Refiere a Manuel Pineyro en tercera persona.""",
                    'error_msg': "No se encontró el CV de Manuel Pineyro."
                },
                'en': {
                    'template': """You are an expert assistant analyzing Manuel Pineyro's CV.
                    
                    The CV contains the following information:
                    {context}
                    
                    Question: {query}
                    
                    Please provide a detailed and objective response in English based on the CV.
                    Avoid using first person. Refer to Manuel Pineyro in third person.""",
                    'error_msg': "Manuel Pineyro's CV was not found."
                }
            }
        else:
            templates = {
                'es': {
                    'template': """Eres un asistente experto analizando el CV de {name}.
                    
                    El CV contiene la siguiente información:
                    {context}
                    
                    Pregunta: {query}
                    
                    Proporciona una respuesta detallada y objetiva en español, basada en el CV.
                    Menciona ejemplos específicos cuando sea relevante.""",
                    'error_msg': "CV no encontrado."
                },
                'en': {
                    'template': """You are an expert assistant analyzing {name}'s CV.
                    
                    The CV contains the following information:
                    {context}
                    
                    Question: {query}
                    
                    Please provide a detailed and objective response in English based on the CV.
                    Mention specific examples when relevant.""",
                    'error_msg': "CV not found."
                }
            }
        
        return templates.get(detected_lang, templates['en']) 