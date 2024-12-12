import streamlit as st
from document_loader import DocumentLoader
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from config import GROQ_API_KEY, LLM_MODEL_NAME
from agents import AgentManager
import os

class ChatbotApp:
    def __init__(self):
        self.loader = DocumentLoader()
        self.agent_manager = AgentManager()
        
        # Cargar todos los CVs del directorio data/cvs
        self.load_all_cvs()
        
        # Inicializar memoria de conversación
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )

    def load_all_cvs(self):
        """Cargar todos los CVs del directorio data/cvs"""
        cv_dir = "data/cvs"
        if not os.path.exists(cv_dir):
            st.error(f"¡No se encontró el directorio {cv_dir}!")
            return

        loaded_cvs = []
        manuel_loaded = False

        for filename in os.listdir(cv_dir):
            if filename.endswith('.pdf'):
                cv_path = os.path.join(cv_dir, filename)
                try:
                    chunks = self.loader.load_pdf(cv_path)
                    cv_text = " ".join(chunks)
                    
                    name = os.path.splitext(filename)[0]
                    
                    is_manuel = name.lower() == "manuel_pineyro"
                    if is_manuel:
                        manuel_loaded = True
                    
                    self.agent_manager.add_agent(
                        name=name,
                        cv_text=cv_text,
                        is_default=is_manuel
                    )
                    loaded_cvs.append(filename)
                except Exception as e:
                    st.error(f"Error al cargar {filename}: {str(e)}")

        if loaded_cvs:
            if not manuel_loaded:
                st.warning("No se encontró el CV de Manuel. Las consultas sin nombre específico no funcionarán.")
            st.success(f"Se cargaron {len(loaded_cvs)} CVs: {', '.join(loaded_cvs)}")
        else:
            st.warning("No se encontraron CVs en el directorio data/cvs")

    def process_query(self, query: str) -> str:
        """Procesar una consulta y devolver la respuesta"""
        try:
            return self.agent_manager.process_query(query)
        except Exception as e:
            return f"Error procesando la consulta: {str(e)}"

def main():
    st.set_page_config(page_title="CV Chatbot", page_icon="📄", layout="wide")
    
    # Sidebar para cargar CVs
    with st.sidebar:
        st.header("Cargar CV")
        uploaded_file = st.file_uploader(
            "Seleccione un archivo PDF",
            type=['pdf'],
            help="Suba un CV en formato PDF"
        )
        
        if uploaded_file is not None:
            # Guardar el archivo subido
            save_path = os.path.join("data/cvs", uploaded_file.name)
            os.makedirs("data/cvs", exist_ok=True)
            
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Reiniciar el chatbot para cargar el nuevo CV
            if 'chatbot' in st.session_state:
                del st.session_state.chatbot
            
            st.success(f"CV cargado exitosamente: {uploaded_file.name}")
            
        # Mostrar CVs cargados
        if os.path.exists("data/cvs"):
            cvs = [f for f in os.listdir("data/cvs") if f.endswith('.pdf')]
            if cvs:
                st.subheader("CVs Disponibles")
                for cv in cvs:
                    st.text(f"📄 {cv}")
            else:
                st.info("No hay CVs cargados")
    
    # Contenido principal
    st.title("CV Chatbot")
    st.write("Haga preguntas sobre los CVs cargados")
    
    # Inicializar estado de la sesión
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotApp()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar mensajes del chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Entrada del chat
    if prompt := st.chat_input("Escriba su pregunta aquí"):
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Obtener respuesta del bot
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = st.session_state.chatbot.process_query(prompt)
                st.markdown(response)
        
        # Agregar respuesta del asistente al historial
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 