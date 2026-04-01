# Chatbot FAMAF

<p align="center">
   <img width="1653" height="516" alt="image" src="https://github.com/user-attachments/assets/cf8a72a8-5299-4bce-942c-485acc002eff" />
</p>

Este repositorio contiene la implementación de un **asistente para WhatsApp** diseñado para atender consultas frecuentes de la comunidad de la **Facultad de Matemática, Astronomía, Física y Computación (FAMAF)** de la **Universidad Nacional de Córdoba**.

<p align="center">
  <a href="https://wa.me/5493513769490?text=Hola!%20Tengo%20una%20consulta%20sobre%20FAMAF" target="_blank">
    <img src="https://img.shields.io/badge/Chat_con_el_Bot-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="Chat en WhatsApp">
  </a>
</p>

## ℹ️ Descripción del Proyecto
El sistema despliega un Agente basado en Recuperación de Información que resuelve consultas sobre trámites, materias y vida académica utilizando respuestas predefinidas, eliminando el riesgo de alucinaciones.

### Características Principales:
* **Arquitectura de Recuperación:** utiliza búsqueda vectorial para contrastar las consultas de los usuarios con una base de conocimiento curada (información extraída de sitios oficiales y redes sociales de la institución).
* **Almacenamiento y Búsqueda de Vectores:** usa índices de **Pinecone** para almacenar los *embeddings* de la base de conocimiento y su motor para la recuperación semántica de información.
* **Automatización de Procesos:** flujos de trabajo automatizados de **n8n** para actualizar la base de conocimiento del agente y responder las consultas entrantes.
* **Observabilidad:** registro y trazabilidad de cada interacción en **Langfuse** para monitorear el comportamiento del agente en tiempo real.
* **Panel de Administración:** interfaz web para gestionar el conocimiento del bot.

## ⚙️ Arquitectura del Sistema
La arquitectura del sistema se divide en componentes. Como introducción de estos componentes y para entender el funcionamiento del sistema, describiremos a continuación brevemente los procesos siguiendo el ciclo de vida de la información:

* **n8n:** es el encargado de que todas las componentes se comuniquen entre sí. Recibe las consultas de los estudiantes a través de _WhatsApp Business API_, realiza las búsquedas de información en Pinecone, para la información recuperada al modelo de lenguaje y le responde al usuario.
* **Pinecone:** es donde se almacena el conocimiento del chatbot. Es la base de datos vectorial que guarda las preguntas frecuentes procesadas en forma de vectores con su respuesta como metadato. Esto permite realizar búsquedas semánticas de manera eficiente para encontrar las consultas más similares a la que realizó el estudiante y que el modelo necesita antes de decidir la respuesta.
* **Redis:** es una base de datos de alta velocidad que utilizamos para llevar la cuenta de cuántas preguntas hace cada usuario en un intervalo determinado y que se consulta antes de procesar la respuesta. Básicamente, guarda el identificador de la persona junto con su número de consultas para evitar abusos y asegurar que el sistema no se sature.
* **Langfuse:** en producción se encarga de registrar cada interacción entre los estudiantes y el agente con la consulta, la respuesta y la latencia. Además, sirve para evaluar las arquitecturas y los modelos con los workflows de `evaluation/` permitiendo analizar el consumo de tokens, calcular métricas y detectar errores.
* **Panel de Administrador:** es una interfaz web pensada para gestionar la base de conocimiento del sistema. Desde acá se puede actualizar o cargar nueva información manualmente o masivamente usando archivos `.csv`, además de revisar las preguntas que ya forman parte del conocimiento del agente.

## 📖 Guía de Instalación

Levantar todo el ecosistema tiene sus detalles (configurar las variables de entorno, iniciar los contenedores de Docker y dejar conectado todo con n8n), es por eso que en **la Wiki del proyecto** vas a encontrar las descripciones de las variables de entorno y las instrucciones necesarias para dejar todo funcionando en un entorno local.

👉 [Ver las instrucciones de instalación paso a paso en la Wiki](https://github.com/mit0110/chatbot_famaf/wiki)

## 🛠️ Requisitos previos
Para desplegar todo el ecosistema (n8n, Redis, Langfuse, Panel de Administrador), el sistema se apoya en una serie de servicios interconectados que se despliegan mediante Docker. 

**Herramientas necesarias:**
* **Docker y Docker Compose:** para levantar todos los contenedores del sistema.
* **Git:** para clonar el repositorio y gestionar las versiones del proyecto.

**Configuración de Entorno:**
Antes de levantar todos los contenedores necesitaremos crear un archivo `.env` siguiendo el ejemplo del directorio `infra/`.

**Credenciales y API Keys** 
Una vez desplegado el proyecto, debemos ingresar a n8n y para crear las credenciales necesitaremos lo siguiente:
* **Pinecone**: para buscar e insertar datos en la base de conocimiento, se necesita de: 
   * Una cuenta en [Pinecone](https://app.pinecone.io/) para obtener una *API KEY* y acceder a la base de datos vectorial.
* **WhatsApp**: para poder enviar y recibir mensajes usando la *WhatsApp Business API* es necesario tener:
   * Un portafolio comercial en [Meta for Business](https://business.facebook.com/).
   * Una cuenta de desarrollador en [Meta for Developers](https://developers.facebook.com/).
   * Una aplicación con el caso de uso "Conectarte con los clientes a través de WhatsApp" asociada al portafolio comercial para conseguir
     * *Identificador* y *Clave Secreta* de la app para recibir mensajes.
     * *Business Account ID* y *Token Permanente* con control total sobre la app para enviar mensajes.
* **Google Gemini API**: para consumir los modelos de Google (modelos de *embeddings* y LLMs), se necesita de:
  * Una cuenta en [Google AI Studio](https://aistudio.google.com/) con un proyecto.
  * Una *API KEY* asociada al proyecto.
* **Langfuse**: para registrar datos desde n8n ya sea en su versión web o la versión self-hosted que se levanta con el infraestructura, se necesita de:
   * *Public Key* y *Secret Key* asociadas a un proyecto.
* **Redis**: para consultar los límites de cada usuario, es necesario tener:
  * Una base de datos creada dentro de Redis que nos dará:
      * *Base de Datos* y *Contraseña* de acceso a esa base de datos.
      * *Host* y *Puerto*.
* **Ollama CCAD (Opcional)**: para usar modelos de Centro de Computación de Alto Desempeño (CCAD) de la Universidad Nacional de Córdoba, se necesita de:
  * Acceso a [chat.ccad.unc.edu.ar](https://chat.ccad.unc.edu.ar/) para generar una *API KEY*.
* **Telegram (Opcional)**: para recibir y enviar mensajes vía Telegram es necesario:
   * Tener una cuenta de Telegram y tener un bot, o bien crearlo usando [Bot Father](https://telegram.me/BotFather).
   * *Token de acceso* al bot.

## 📂 Estructura del repositorio
La organización de las carpetas dentro del proyecto es la siguiente:

```text
├── admin_panel/
├── data/
├── infra/
├── notebooks/
└── workflows/
    ├── canned_responses/
    ├── rag/
    └── evaluation/
```

* **`admin_panel/`**: Contiene el **código de la interfaz web** para gestionar la base de conocimiento del bot.
* **`data/`**: Almacena las **bases de conocimiento y los conjuntos de datos** que utilizamos durante el desarrollo y la evaluación del chatbot.
* **`infra/`**: Todo lo relacionado con la infraestructura y el despliegue del ecosistema (archivo Docker Compose y `.env` de ejemplo para su configuración).
* **`notebooks/`**: Incluye los ***Jupyter Notebooks* utilizados para calcular métricas, evaluar resultados y analizar el comportamiento del sistema**.
* **`workflows/`**: Acá están exportados **todos los flujos de n8n que implementan la lógica del sistema**, divididos según su propósito:
  * **`canned_responses/`**: Arquitectura de un chatbot con respuestas predefinidas (**versión de producción**).
  * **`rag/`**: Flujos que implementan una arquitectura RAG (Retrieval-Augmented Generation) en una versión experimental. 
  * **`evaluation/`**: Flujos creados para automatizar la evaluación y calcular métricas de las distintas versiones del chatbot que se desarrollaron a lo largo del proyecto.
