# chatbot_famaf

<p align="center">
   <img width="1653" height="516" alt="image" src="https://github.com/user-attachments/assets/cf8a72a8-5299-4bce-942c-485acc002eff" />
</p>
<p align="center">
  <a href="https://t.me/FAMAFBot">
    <img src="https://img.shields.io/badge/Chat_con_el_Bot-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Chat en Telegram">
  </a>
</p>

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
