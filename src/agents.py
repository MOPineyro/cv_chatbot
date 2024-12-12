from typing import List, Dict, Optional
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from vector_store import VectorStore
from config import GROQ_API_KEY, LLM_MODEL_NAME
from name_extractor import NameExtractor
from language_detector import LanguageDetector

class CVAgent:
    def __init__(self, name: str, full_name: str, namespace: str):
        """
        Inicializar un agente para un CV específico
        """
        self.name = name
        self.full_name = full_name
        self.namespace = namespace
        self.vector_store = VectorStore(namespace=namespace)
        
        print(f"Agente creado para {full_name} en namespace: {namespace}")

    def add_cv_text(self, cv_text: str):
        """Agregar el texto del CV al vector store"""
        # Dividir el texto en chunks más significativos
        chunks = []
        lines = cv_text.split('\n')
        current_chunk = []
        current_length = 0
        
        for line in lines:
            if len(line.strip()) == 0:
                continue
            
            # Si es un encabezado o sección nueva
            if line.isupper() or line.endswith(':'):
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_length = 0
            
            current_chunk.append(line.strip())
            current_length += len(line)
            
            # Si el chunk actual es suficientemente grande
            if current_length >= 500:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
        
        # Agregar el último chunk si existe
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Agregar metadatos para mejorar la búsqueda
        metadatas = []
        for chunk in chunks:
            metadata = {
                "cv_name": self.full_name,
                "section": self._identify_section(chunk),
                "content_type": self._identify_content_type(chunk)
            }
            metadatas.append(metadata)
        
        # Agregar chunks al vector store
        print(f"\nAgregando {len(chunks)} chunks al vector store para {self.full_name}")
        for i, (chunk, meta) in enumerate(zip(chunks, metadatas)):
            print(f"\nChunk {i+1}:")
            print(f"Sección: {meta['section']}")
            print(f"Tipo: {meta['content_type']}")
            print(f"Contenido: {chunk[:100]}...")
        
        self.vector_store.add_texts(chunks, metadatas)

    def _identify_section(self, text: str) -> str:
        """Identificar la sección del CV a la que pertenece el texto (español/inglés)"""
        text = text.lower()
        
        # Mapeo de secciones en ambos idiomas
        sections = {
            'experiencia': [
                # Español
                'experiencia', 'trabajo', 'empleo', 'trayectoria', 'carrera', 'laboral',
                # Inglés
                'experience', 'work', 'employment', 'career', 'professional'
            ],
            'educación': [
                # Español
                'educación', 'formación', 'estudios', 'académico', 'título',
                # Inglés
                'education', 'academic', 'degree', 'studies', 'university'
            ],
            'habilidades': [
                # Español
                'habilidades', 'tecnologías', 'competencias', 'conocimientos', 'destrezas',
                # Inglés
                'skills', 'technologies', 'competencies', 'expertise', 'proficiencies', 'tech stack'
            ],
            'proyectos': [
                # Español
                'proyectos', 'logros', 'desarrollos',
                # Inglés
                'projects', 'achievements', 'developments', 'portfolio'
            ],
            'resumen': [
                # Español
                'resumen', 'perfil', 'sobre mí', 'acerca de',
                # Inglés
                'summary', 'profile', 'about me', 'overview', 'professional summary'
            ]
        }
        
        # Buscar coincidencias en cada sección
        for section, keywords in sections.items():
            if any(kw in text for kw in keywords):
                return section
            
        return 'general'

    def _identify_content_type(self, text: str) -> str:
        """Identificar el tipo de contenido del chunk (español/inglés)"""
        text = text.lower()
        
        # Mapeo de tipos de contenido en ambos idiomas
        content_types = {
            'tecnologías': [
                # Lenguajes de programación y frameworks
                'python', 'java', 'javascript', 'typescript', 'react', 'node', 'angular',
                'vue', 'django', 'flask', 'spring', 'aws', 'azure', 'docker', 'kubernetes',
                # Palabras clave en ambos idiomas
                'programación', 'programming', 'desarrollo', 'development', 'código', 'code',
                'software', 'aplicación', 'application', 'api', 'web', 'móvil', 'mobile'
            ],
            'educación': [
                # Español
                'universidad', 'título', 'grado', 'máster', 'doctorado', 'licenciatura',
                'ingeniería', 'certificación',
                # Inglés
                'university', 'degree', 'bachelor', 'master', 'phd', 'certification',
                'engineering', 'college', 'school'
            ],
            'liderazgo': [
                # Español
                'lideré', 'dirigí', 'gestioné', 'coordiné', 'supervisé', 'equipo',
                'gestión', 'dirección',
                # Inglés
                'led', 'managed', 'coordinated', 'supervised', 'team', 'leadership',
                'management', 'direction'
            ],
            'logros': [
                # Español
                'logré', 'conseguí', 'implementé', 'mejoré', 'optimicé', 'reduje',
                'aumenté', 'desarrollé',
                # Inglés
                'achieved', 'implemented', 'improved', 'optimized', 'reduced',
                'increased', 'developed', 'delivered'
            ]
        }
        
        # Buscar coincidencias en cada tipo de contenido
        for content_type, keywords in content_types.items():
            if any(kw in text for kw in keywords):
                return content_type
            
        return 'general'

    def get_context(self, query: str, k: int = 3) -> List[Dict]:
        """
        Obtener contexto relevante del CV para una consulta
        """
        print(f"\nBuscando en namespace: {self.namespace}")
        return self.vector_store.similarity_search(query, k=k)

class AgentManager:
    def __init__(self):
        """
        Inicializar el gestor de agentes
        """
        self.agents: Dict[str, CVAgent] = {}
        self.default_agent: Optional[CVAgent] = None
        self.name_extractor = NameExtractor()
        self.name_mappings: Dict[str, str] = {}  # mapeo de variaciones a nombres canónicos
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=LLM_MODEL_NAME,
            temperature=0.7
        )
        
    def add_agent(self, name: str, cv_text: str, is_default: bool = False):
        """Agregar un nuevo agente al sistema"""
        # Extraer nombre completo del CV
        full_name = self.name_extractor.extract_name_from_cv(cv_text) or name
        
        # Crear variaciones del nombre
        self._add_name_mappings(name, full_name)
        
        # Crear agente
        namespace = f"cv_{name.lower()}"
        agent = CVAgent(
            name=name,
            full_name=full_name,
            namespace=namespace
        )
        
        # Agregar texto del CV al vector store
        agent.add_cv_text(cv_text)
        
        self.agents[name.lower()] = agent
        
        # Establecer como predeterminado si corresponde
        if name.lower() == "manuel_pineyro" or (is_default and not self.default_agent):
            self.default_agent = agent
            print(f"Agente predeterminado establecido: {full_name}")

    def _add_name_mappings(self, name: str, full_name: str):
        """
        Agregar variaciones de nombres al mapeo
        """
        name_parts = full_name.lower().split()
        
        for part in name_parts:
            self.name_mappings[part] = name.lower()
        
        for i in range(len(name_parts)-1):
            combined = " ".join(name_parts[i:i+2])
            self.name_mappings[combined] = name.lower()
        
        self.name_mappings[full_name.lower()] = name.lower()
        self.name_mappings[name.lower()] = name.lower()
        
        if len(name_parts) > 1:
            last_name = name_parts[-1]
            self.name_mappings[last_name] = name.lower()
            
            if len(name_parts) > 2:
                compound_last_name = " ".join(name_parts[-2:])
                self.name_mappings[compound_last_name] = name.lower()
                self.name_mappings[name_parts[-2]] = name.lower()
        
        print(f"Name mappings for {full_name}: {self.name_mappings}")

    def get_prompt(self, context: List[Dict], query: str, agent_name: str = None) -> str:
        """
        Generar el prompt para el LLM basado en el idioma de la consulta
        """
        detected_lang = LanguageDetector.detect_language(query)
        template_data = LanguageDetector.get_response_template(
            detected_lang,
            is_default_agent=(agent_name is None)
        )
        
        context_text = "\n".join([f"- {item['text']}" for item in context])
        return template_data['template'].format(
            name=agent_name,
            context=context_text,
            query=query
        )
        
    def extract_names(self, query: str) -> List[str]:
        """
        Extraer nombres mencionados en la consulta usando el LLM
        """
        prompt = """
        De la siguiente consulta, extrae los nombres de las personas mencionadas.
        Si no hay nombres mencionados, responde con una lista vacía.
        Responde solo con los nombres encontrados, separados por comas.
        
        Nombres conocidos y sus variaciones:
        {known_names}
        
        Consulta: {query}
        
        Importante: Solo devolver nombres que estén en la lista de nombres conocidos.
        """
        
        # Crear lista de nombres conocidos con todas sus variaciones
        known_names_list = []
        for agent in self.agents.values():
            known_names_list.append(f"- {agent.full_name} (variaciones: {', '.join(k for k, v in self.name_mappings.items() if v == agent.name.lower())})")
        
        known_names = "\n".join(known_names_list)
        print(f"Buscando entre los nombres: {known_names}")  # Debug
        
        try:
            result = self.llm.predict(prompt.format(
                known_names=known_names,
                query=query
            ))
            
            extracted = [name.strip().lower() for name in result.split(',') if name.strip()]
            print(f"Nombres extraídos: {extracted}")  # Debug
            
            mentioned_names = []
            for name in extracted:
                if name in self.name_mappings:
                    mentioned_names.append(self.name_mappings[name])
            
            print(f"Nombres mapeados: {mentioned_names}")  # Debug
            return list(set(mentioned_names))
        except Exception as e:
            print(f"Error extrayendo nombres: {str(e)}")
            return []
        
    def process_query(self, query: str) -> str:
        """
        Procesar una consulta y obtener respuesta
        """
        mentioned_names = self.extract_names(query)
        print(f"Nombres detectados en la consulta: {mentioned_names}")  # Debug
        
        if not mentioned_names:
            if not self.default_agent:
                return "No se encontró el CV de Manuel ni hay otro agente predeterminado configurado."
            print(f"Usando agente predeterminado: {self.default_agent.full_name}")  # Debug
            context = self.default_agent.get_context(query)
            prompt = self.get_prompt(context, query)
            return self.llm.predict(prompt)
            
        if len(mentioned_names) == 1:
            name = mentioned_names[0]
            if name not in self.agents:
                return f"No se encontró el CV de {name}"
            
            agent = self.agents[name]
            print(f"Usando agente para {agent.full_name}")  # Debug
            context = agent.get_context(query)
            prompt = self.get_prompt(context, query, agent.full_name)
            return self.llm.predict(prompt)
            
        # Caso múltiple: obtener contexto de todos los CVs mencionados
        all_context = []
        names = []
        for name in mentioned_names:
            if name in self.agents:
                agent = self.agents[name]
                context = agent.get_context(query)
                all_context.extend(context)
                names.append(agent.full_name)
        
        if not names:
            return "No se encontraron los CVs mencionados"
        
        prompt = self.get_prompt(all_context, query, ", ".join(names))
        return self.llm.predict(prompt) 