import streamlit as st
from document_loader import DocumentLoader
from vector_store import VectorStore
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from config import GROQ_API_KEY, LLM_MODEL_NAME
import os

class ChatbotApp:
    def __init__(self):
        self.loader = DocumentLoader()
        self.vector_store = VectorStore()
        
        # Cargar todos los CVs del directorio data/cvs
        self.load_all_cvs()
        
        # Inicializar el modelo LLM de Groq
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=LLM_MODEL_NAME,
            temperature=0.7,
            max_tokens=4096
        )
        
        # Inicializar memoria de conversación
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )
        
        # Inicializar la cadena RAG
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.get_retriever(),
            memory=self.memory,
            return_source_documents=True,
            return_generated_question=True,
            combine_docs_chain_kwargs={"prompt": self.get_prompt()}
        )

    def load_all_cvs(self):
        """Cargar todos los CVs del directorio data/cvs"""
        cv_dir = "data/cvs"
        if not os.path.exists(cv_dir):
            st.error(f"¡No se encontró el directorio {cv_dir}!")
            return

        all_chunks = []
        loaded_cvs = []

        for filename in os.listdir(cv_dir):
            if filename.endswith('.pdf'):
                cv_path = os.path.join(cv_dir, filename)
                try:
                    chunks = self.loader.load_pdf(cv_path)
                    all_chunks.extend(chunks)
                    loaded_cvs.append(filename)
                except Exception as e:
                    st.error(f"Error al cargar {filename}: {str(e)}")

        if all_chunks:
            try:
                self.vector_store.add_texts(all_chunks)
                st.success(f"Se cargaron {len(loaded_cvs)} CVs: {', '.join(loaded_cvs)}")
            except Exception as e:
                st.error(f"Error al agregar textos al almacén vectorial: {str(e)}")
        else:
            st.warning("No se encontraron CVs en el directorio data/cvs")

    def get_prompt(self):
        """Obtener el prompt personalizado para el chatbot"""
        template = """Eres un asistente útil que responde preguntas sobre CVs.
        Usa la siguiente información para responder la pregunta del usuario:
        {context}
        
        Pregunta: {question}
        
        Respuesta útil:"""
        
        from langchain.prompts import PromptTemplate
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

    def process_query(self, query: str) -> str:
        """Procesar una consulta y devolver la respuesta"""
        try:
            result = self.qa_chain({"question": query})
            return result['answer']
        except Exception as e:
            return f"Error procesando la consulta: {str(e)}"

def main():
    st.set_page_config(page_title="CV Chatbot", page_icon="📄")
    
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