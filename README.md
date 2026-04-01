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

* **n8n:** Es el encargado de que todas las componentes se comuniquen entre sí. Recibe las consultas de los estudiantes a través de _WhatsApp Business API_, realiza las búsquedas de información en Pinecone, para la información recuperada al modelo de lenguaje y le responde al usuario.
* **Pinecone:** Es donde se almacena el conocimiento del chatbot. Es la base de datos vectorial que guarda las preguntas frecuentes procesadas en forma de vectores con su respuesta como metadato. Esto permite realizar búsquedas semánticas de manera eficiente para encontrar las consultas más similares a la que realizó el estudiante y que el modelo necesita antes de decidir la respuesta.
* **Langfuse:** En producción se encarga de registrar cada interacción entre los estudiantes y el agente con la consulta, la respuesta y la latencia. Además, sirve para evaluar las arquitecturas y los modelos con los workflows de `evaluation/` permitiendo analizar el consumo de tokens, calcular métricas y detectar errores.
* **Panel de Administrador:** Es una interfaz web pensada para gestionar la base de conocimiento del sistema. Desde acá se puede actualizar o cargar nueva información manualmente o masivamente usando archivos `.csv`, ademmás de revisar las preguntas que ya forman parte del conocimiento del agente.

## 📋 Tabla de Contenidos

1. [Importar y Configurar los Workflows RAG](#-importar-y-configurar-los-workflows-rag)
   - [Pasos para importar](#pasos-para-importar)
   - [Configuración de Credenciales](#-configuración-de-credenciales)
2. [Configurar un Webhook de Telegram en n8n (Local)](#%EF%B8%8F-configurar-un-webhook-de-telegram-en-n8n-local-para-recibir-mensajes-del-bot)
   - [Requisitos previos](#1-requisitos-previos)
   - [Configurar ngrok y .env](#2-configurar-ngrok-y-actualizar-el-archivo-env)
   - [Ubicar el nodo Trigger](#3-ubicar-y-verificar-el-nodo-trigger-en-rag_query)
   - [Credenciales de Telegram](#4-configurar-las-credenciales-de-telegram)
   - [Probar la recepción](#5-probar-la-recepción-de-mensajes)
3. [Configuración del Entorno](#%EF%B8%8F-configuración-del-entorno)
   - [Permisos para la librería Crypto](#permisos-para-la-librería-crypto)

---

## 📥 Importar y Configurar los Workflows RAG

En el repositorio, dentro de la carpeta `workflows/rag`, encontrarás los archivos necesarios para desplegar la lógica del chatbot. Deberás importar los siguientes dos archivos `.json`:

1.  **`rag_ingestion.json`**: Este flujo se encarga de leer la información, generar los embeddings y cargarlos en la base de datos vectorial.
2.  **`rag_query.json`**: Este es el flujo principal del bot (el que se ve en las imágenes) que recibe el mensaje de Telegram, consulta la base de datos y genera la respuesta usando un modelo generativo.

### Pasos para importar:

1.  Descargá los archivos `.json` del repositorio a tu computadora.
2.  Abrí tu instancia de n8n.
3.  En el menú de workflows (o desde la pantalla principal), buscá la opción **"Import from File"** (o "Importar desde archivo").
4.  Seleccioná y cargá ambos archivos.

---

### 🔑 Configuración de Credenciales

Una vez importados los workflows, notarás que algunos nodos pueden marcar errores o pedir autenticación. Para que todo funcione, es **indispensable** dar de alta y configurar las siguientes credenciales dentro de n8n:

* **Telegram API:** Necesaria para el nodo *Telegram Trigger* (recibir mensajes) y los nodos de respuesta.
* **Google Gemini API:** Requerida para:
    * El **Chat Model**.
    * El nodo de **Embeddings** (para vectorizar las preguntas y documentos).
* **Pinecone API:** Necesaria para conectar con el nodo *Vector Store*, donde se almacenan y buscan los datos de conocimiento.
* **GitHub API:** Requerida en el workflow de ingestión (`rag_ingestion.json`) para poder acceder y leer el conjunto de datos directamente desde este repositorio.
* **OpenAi API**: se utiliza para el workflow (rag_query_ollama_ccad.json), la credencial debe ser configurada como:
    * base URL : https://chat.ccad.unc.edu.ar/ollama/v1
    * API Key: acceder a su cuenta de https://chat.ccad.unc.edu.ar/ > Ajustes > Cuenta > Claves API y copiar la clave disponible 

> **Nota importante:** Para comenzar a recibir mensajes de Telegram en la instancia local, seguir los pasos detallados en la sección [Configurar un Webhook de Telegram en n8n (Local) para Recibir Mensajes del Bot](#%EF%B8%8F-configurar-un-webhook-de-telegram-en-n8n-local-para-recibir-mensajes-del-bot)

---

## ⚙️ Configurar un Webhook de Telegram en n8n (Local) para Recibir Mensajes del Bot

El nodo *trigger* que inicia el flujo `rag_query` necesita soporte SSL para recibir los mensajes de Telegram. Como n8n se ejecuta en un entorno local, utilizaremos **ngrok** para crear un dominio público y exponer el puerto de n8n.

### 1. Requisitos previos

Antes de continuar, es necesario tener instalado **n8n usando Docker Compose**. Podés seguir la [guía oficial](https://docs.n8n.io/hosting/installation/server-setups/docker-compose/#4-create-an-env-file).

Si seguiste ese proceso, ya deberías contar con un directorio que incluya:
- un archivo `.yml`
- un archivo `.env`

También necesitás tener instalado [ngrok](https://ngrok.com/download).

---

### 2. Configurar ngrok y actualizar el archivo `.env`

1. Iniciá sesión en tu cuenta de ngrok.
2. Desde el *dashboard*, ingresá a la sección **Domains**.
3. Allí verás un dominio asignado automáticamente.
4. Hacé clic sobre el dominio y copiá **solo el subdominio** (la parte antes del primer punto).
5. Reemplazá los valores de `SUBDOMAIN` y `DOMAIN_NAME` en tu archivo `.env` de n8n de la siguiente forma:

```env
# DOMAIN_NAME and SUBDOMAIN together determine where n8n will be reachable from
DOMAIN_NAME=ngrok-free.dev
SUBDOMAIN=tu-subdominio-copiado-de-ngrok

# Optional timezone
GENERIC_TIMEZONE=America/Argentina/Buenos_Aires

# The email address to use for the TLS/SSL certificate creation
SSL_EMAIL=user@example.com
```

Una vez modificado este archivo, reiniciá los contenedores:
```bash
docker compose down
docker compose up -d
```

---

### 3. Ubicar y verificar el nodo Trigger en `rag_query`

1. Abrí n8n y entrá al workflow **`rag_query`** (que importaste anteriormente).
2. Localizá el primer nodo del flujo, llamado **"Cuando Reciba un Mensaje"** (Telegram Trigger).
3. Hacé doble clic para abrir su configuración.
4. En la sección **Webhook URLs**, deberías ver el dominio que configuraste en el archivo `.env` (el dominio de ngrok).

---

### 4. Configurar las credenciales de Telegram

Dentro del mismo nodo Trigger que acabas de abrir:

1. Buscá el apartado **Credentials**.
2. Seleccioná "Create New" (o elegí la credencial si ya la creaste para otro flujo).
3. Pegá el **Access Token** del bot de Telegram.

---

### 5. Probar la recepción de mensajes

Para confirmar que el flujo `rag_query` recibe los mensajes:

1. En el nodo trigger ("Cuando Reciba un Mensaje"), hacé clic en el botón **Execute Step** (o "Listen for Event").
2. Enviá un mensaje al bot de Telegram.
3. Deberías ver que el nodo captura los datos del mensaje (User ID, texto, fecha, etc.) dentro de n8n.

> **Nota importante:** Una vez verificado, no olvides activar el interruptor **"Active"** (arriba a la derecha del canvas) para que el bot responda automáticamente sin que tengas que ejecutarlo manualmente.

## ⚙️ Configuración del Entorno
### Permisos para la Librería Crypto
Para el almacenamiento de trazas vía [OTLP](https://opentelemetry.io/docs/specs/otlp/#otlphttp) dentro de LangFuse, realizado en el flujo de trabajo `generate_traces`, es necesario generar UUIDs. Para cumplir con este requisito, se utiliza el método `randomUUID` del módulo nativo `crypto` de Node.js.

Dado que n8n restringe la importación de módulos nativos por seguridad, es necesario levantar esa restricción para este módulo específico, añadiendo la siguiente variable de entorno al servicio de n8n en el archivo `compose.yml:

```yaml
  n8n:
    image: docker.n8n.io/n8nio/n8n
    environment:
      # Habilita el uso de la librería nativa 'crypto' en los nodos de código
      - NODE_FUNCTION_ALLOW_BUILTIN=crypto
    # ... resto de la configuración
```
