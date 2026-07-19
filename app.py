import streamlit as st
import os
import warnings
from dotenv import load_dotenv

# Cargar variables de entorno primero
load_dotenv()

# Silenciar advertencias de obsolescencia en la consola
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict

# Configuración de la página
st.set_page_config(
    page_title="Agente Bim Bam Bui", 
    page_icon="🕷️",
    layout="centered"
)

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🕷️ Agente Virtual Bim Bam Bui")
st.caption("Asistente inteligente de e-commerce enfocado en una experiencia de compra ágil y segura.")

@st.cache_resource
def inicializar_agente_y_datos():
    # SOLUCIÓN ADVERTENCIA 1: Priorizar GEMINI_API_KEY explícitamente para evitar conflictos
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite", 
        temperature=0, 
        google_api_key=api_key
    )
    
    archivos_pdf = [
        "MetodosPago.pdf",
        "GarantiaProductos.pdf",
        "TiemposCostosEnvio.pdf",
        "ProgramaAfiliados.pdf",
        "PoliticaReembolsosDevoluciones.pdf"
    ]
    
    docs = []
    for file in archivos_pdf:
        if os.path.exists(file):
            loader = PyPDFLoader(file)
            docs.extend(loader.load())
        
    if not docs:
        st.error("No se encontraron los archivos PDF de soporte en el directorio actual.")
        st.stop()
        
    clean_docs = [
        Document(
            page_content=" ".join(doc.page_content.replace("-","-").split()),
            metadata=doc.metadata
        )
        for doc in docs
    ]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=250
    )
    documents = text_splitter.split_documents(clean_docs)
    
    # El token se pasa automáticamente si está configurado en tu archivo .env como HF_TOKEN
    model_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ) 
    vectorstore = FAISS.from_documents(documents, model_embeddings)
    
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4},
        search_type="similarity"
    )
    
    prompt_rag = ChatPromptTemplate.from_messages([
        ("system", """
Eres el agente virtual experto de Bim Bam Bui, una agencia de e-commerce ágil y segura. Tu objetivo es resolver las dudas de los clientes con total precisión, amabilidad y profesionalismo.

[REGLAS CRÍTICAS DE CONTEXTO]
- Tu única fuente de verdad son los fragmentos de texto provistos en el campo "Contexto".
- Si el contexto responde completamente la pregunta, redacta una respuesta clara, estructurada y natural.
- Si el contexto solo responde una parte de la consulta, entrega la información disponible sin asumir el resto.
- Si el contexto no contiene la respuesta o no está relacionado, responde EXACTAMENTE con esta frase: "No tengo esa información". 
"""),
        ("human", "Contexto:{context}\nPregunta del cliente:{input}")
    ])

    document_chain = prompt_rag | llm
    return retriever, document_chain

retriever, document_chain = inicializar_agente_y_datos()

def busqueda_de_respuestas(pregunta: str) -> Dict:
    related_docs = retriever.invoke(pregunta)
    if not related_docs:
        return {"respuesta": "No tengo esa información", "documentos_relacionados": [], "documentos_encontrados": False}

    contexto_texto = "\n\n".join([doc.page_content for doc in related_docs])
    response = document_chain.invoke({
        "input": pregunta, 
        "context": contexto_texto
    })

    answer = str(response.content[0].get("text", response.content[0])) if isinstance(response.content, list) else str(response.content)

    if answer.rstrip(".!? ").strip() == "No tengo esa información":
        return {"respuesta": "No tengo esa información", "documentos_relacionados": [], "documentos_encontrados": False}

    return {"respuesta": answer, "documentos_relacionados": related_docs, "documentos_encontrados": True}

# Interfaz de botones
st.markdown("### 📌 Consultas Frecuentes")
col_a, col_b, col_c, col_d, col_e = st.columns(5)
pregunta_sugerida = None

with col_a:
    if st.button("📋 Ver Garantias de Productos"): pregunta_sugerida = "Garantias de Productos"
with col_b:
    if st.button("💰 Métodos de Pago"): pregunta_sugerida = "Métodos de pago"
with col_c:
    if st.button("📦 Tiempos y Costos de Envío"): pregunta_sugerida = "¿Cuáles son los costos y tiempos de envío?"
with col_d:
    if st.button("🔄 Política de Reembolsos"): pregunta_sugerida = "Política de reembolsos y devoluciones"
with col_e:      
    if st.button("🤝 Programa de Afiliados"): pregunta_sugerida = "Programa de afiliados"
    
pregunta_usuario = st.chat_input("Escribe tu consulta aquí...")
pregunta_final = pregunta_usuario or pregunta_sugerida

if pregunta_final:
    with st.chat_message("user"):
        st.write(pregunta_final)
        
    with st.chat_message("assistant", avatar="🕷️"):
        with st.spinner("Consultando manuales internos..."):
            resultado = busqueda_de_respuestas(pregunta_final)
            
        st.markdown(resultado['respuesta'])
        
        if resultado['documentos_encontrados'] and resultado['documentos_relacionados']:
            st.write("---")
            st.caption("📄 **Documentos de referencia consultados:**")
            for i, doc in enumerate(resultado['documentos_relacionados']):
                nombre_fuente = os.path.basename(doc.metadata.get('source', f'Documento {i+1}'))
                num_pagina = doc.metadata.get('page', 0) + 1
                with st.expander(f"🔍 {nombre_fuente} — Página {num_pagina}"):
                    st.write(doc.page_content)