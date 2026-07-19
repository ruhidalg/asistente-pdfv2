# 🤖 Asistente PDF — Asistente Virtual Inteligente (RAG)

Un chatbot avanzado potenciado por Inteligencia Artificial que responde de forma automatizada preguntas complejas basándose en documentos PDF cargados por el usuario. 

El agente utiliza una arquitectura **RAG (Retrieval-Augmented Generation)** para buscar fragmentos de texto relevantes dentro de los documentos oficiales y generar respuestas precisas, contextualizadas y con fuentes verificables.

## 🏗️ Arquitectura de la Solución

```text
 ┌────────────────────────────────────────────────────────┐
 │                   Streamlit (Frontend)                 │
 │       ┌────────────────────────────────────────┐       │
 │       │  • Interfaz de Chat interactiva        │       │
 │       │  • Carga de documentos PDF locales     │       │
 │       └───────────────────┬────────────────────┘       │
 └───────────────────────────┼────────────────────────────┘
                             │
                             ▼ [Texto e Ingesta]
 ┌────────────────────────────────────────────────────────┐
 │                LangChain RAG (Pipeline)                │
 │   • Procesamiento de PDF (PyPDF)                       │
 │   • Segmentación de texto (Text Splitter)              │
 └───────────────┬────────────────────────┬───────────────┘
                 │                        │
                 ▼ [Embeddings Semánticos]  ▼ [Prompt + Contexto]
 ┌──────────────────────────────┐  ┌──────────────────────┐
 │       FAISS VectorStore      │  │    Google Gemini     │
 │  • Base de datos local       │  │  • Modelo LLM        │
 │  • Indexación y búsqueda     │  │  • Síntesis de       │
 │    de similitud rápida       │  │    respuestas        │
 └──────────────────────────────┘  └──────────────────────┘
```
**Flujo de trabajo paso a paso:**

* **Ingesta:** El usuario carga un documento PDF a través de la interfaz de Streamlit. El sistema extrae el texto usando `pypdf`.
* **Indexación:** El texto se divide en fragmentos pequeños y se convierte en vectores usando embeddings de `langchain-huggingface` para guardarse en la base vectorial FAISS.
* **Recuperación:** Cuando el usuario hace una pregunta, FAISS busca de forma local los fragmentos de texto semánticamente más cercanos a la duda.
* **Generación:** LangChain inyecta esos fragmentos como contexto en un prompt optimizado y `langchain-google-genai` (Gemini) genera una respuesta final precisa y fundamentada.

## 💻 Tecnologías y Herramientas

| Componente | Tecnología | ¿Para qué sirve? |
| :--- | :--- | :--- |
| **Lenguaje** | Python 3.11+ | Base del ecosistema de desarrollo y ejecución. |
| **Interfaz de Usuario** | Streamlit | Frontend dinámico para el chat y el cargador de archivos. |
| **Orquestador RAG** | LangChain | Conexión e infraestructura del pipeline de búsqueda y generación. |
| **Procesamiento de PDF**| PyPDF | Extracción y lectura del contenido textual de los archivos. |
| **Base de Datos Vectorial**| FAISS | Indexación de vectores en memoria local para búsquedas ultrarrápidas. |
| **Embeddings** | HuggingFace (`langchain-huggingface`) | Conversión de texto a vectores de alta densidad semántica. |
| **IA Generativa** | Google Gemini (`langchain-google-genai`) | Razonamiento y redacción de respuestas inteligentes. |

## 🚀 Instrucciones para Ejecutar

Sigue estos pasos para levantar la aplicación en tu entorno local de desarrollo de forma segura:

### 1. Clonar el repositorio e ingresar

git clone [https://github.com/ruhidalg/asistente-pdfv2.git](https://github.com/ruhidalg/asistente-pdfv2.git)

cd asistente-pdfv2

El repositorio incluye archivos pdf que serar cargados para responder preguntas.

### 2. Configurar el entorno virtual de Python
Crear entorno virtual:
python -m venv .venv

Activar entorno (Windows):
.venv\Scripts\activate

Activar entorno (Linux/macOS):
source .venv/bin/activate

### 3. Instalar las dependencias del proyecto
pip install -r requirements.txt

### 4. Configurar las Variables de Env / Secretos
Crea un archivo llamado .env en la raíz de tu proyecto e introduce tus credenciales de API correspondientes:

GEMINI_API_KEY=tu_google_gemini_api_key_aqui
HF_TOKEN=tu_huggingface_token_aqui
⚠️ Nota de Seguridad: El archivo .env se encuentra configurado explícitamente dentro del archivo .gitignore. Jamás comites ni subas este archivo a GitHub para resguardar la confidencialidad de tus API Keys.

### 5. Lanzar la aplicación
streamlit run app.py
El servidor web local se iniciará automáticamente. Puedes acceder de forma manual abriendo http://localhost:8501 en tu navegador.

### 💬 Aplicacion en entorno local
<img width="1916" height="1028" alt="Capturalocal" src="https://github.com/user-attachments/assets/6df9b3a5-a95b-4128-af90-e266237bfa3a" />


### 📝 Ejemplo de Prguentas y respuestas egneradas:

## Pregunta: "Garantias de Productos"

## Respuesta del Asistente:
¿Qué cubre nuestra garantía? La garantía es nuestro compromiso de revisar y resolver fallas atribuibles al producto cuando este ha sido utilizado en condiciones normales (es decir, siguiendo las instrucciones y capacidades del mismo). Esto incluye defectos de fabricación, materiales o ensamblaje que no hayan sido causados por el cliente.

¿Qué no cubre? La garantía no aplica en casos de uso indebido, lo cual incluye manipulación, instalación, carga, almacenamiento o uso fuera de las especificaciones del producto.

¿Cómo se gestiona un reclamo?

Evaluación: Realizamos una revisión justa y trazable coordinada por nuestros equipos de Postventa, Logística y Atención al Cliente.
Daños en tránsito: Si el producto llegó dañado, debes reportarlo dentro de las 48 horas posteriores a la recepción. En estos casos, puede aplicar devolución, cambio o reemplazo sin necesidad de un diagnóstico técnico, siempre que la evidencia sea suficiente.
Reemplazos: Si se aprueba un reemplazo, el nuevo producto conservará la cobertura que aplique por norma local o política interna. Si el reemplazo no es exacto, buscaremos uno equivalente en función, categoría y disponibilidad.
Logística: Si la garantía requiere el retorno físico del producto, la logística se gestionará conforme a nuestra Política de Reembolsos y Devoluciones.
Puntos clave a considerar:

Si el producto presenta una falla posterior a la entrega, el caso se manejará primero bajo el Manual de Garantía.
En caso de dudas sobre si el daño ocurrió en tránsito o es una falla de funcionamiento, nuestro equipo determinará la causa más probable basándose en el momento de detección, el tipo de daño, la evidencia presentada, la condición del embalaje y el historial de transporte.
Si tienes un caso específico o necesitas reportar una falla, por favor proporciónanos los detalles de qué ocurrió, cuándo ocurrió, la condición del producto y si hubo factores externos visibles para poder asistirte mejor.

## Pregunta: "¿Cuáles son los costos y tiempos de envío?"

## Respuesta del Asistente: Costos de envío
El costo final de tu envío se calcula considerando los siguientes factores:

Destino del paquete.
Peso volumétrico y tamaño del paquete.
Servicio elegido.
Promociones vigentes y el umbral de envío gratis (cuando aplique).
Es importante mencionar que el costo total siempre se mostrará antes de que confirmes tu compra. Respecto al envío gratis, este puede ofrecerse bajo condiciones promocionales o montos mínimos definidos por país y campaña; ten en cuenta que puede estar sujeto a categorías, regiones, límites de vigencia o stock.

Tiempos de envío
Los tiempos de entrega son estimados y pueden variar debido a:

Casos especiales: En campañas de alta demanda, lanzamientos o validaciones adicionales, los tiempos pueden ser superiores a los estimados. En estos casos, nos comprometemos a mantenerte informado.
Preparación avanzada: Algunos pedidos requieren validaciones previas (como verificación de identidad, datos fiscales o disponibilidad de inventario), lo cual puede afectar el tiempo de salida sin que esto signifique un problema con tu orden.
Escenarios logísticos: Factores como zonas extendidas o condiciones de acceso pueden influir en el plazo de entrega, sobre lo cual te mantendremos al tanto con un seguimiento activo.
Si tienes alguna duda adicional sobre un pedido específico, no dudes en consultarme. ¡Estamos aquí para ayudarte!

### 💬 Aplicacion en la nube
https://asistente-pdfv2-zj7qxfizpgt8wmbtpam6ks.streamlit.app/
<img width="1917" height="1030" alt="CapturaNube" src="https://github.com/user-attachments/assets/87d5e61b-aa57-420a-abf3-9b485249e05c" />

En repositorio se adjunto video de uso.
