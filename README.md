# chatbot_famaf

## Configurar un Webhook de Telegram en n8n (Local) para Recibir Mensajes del Bot

El nodo *tigger* `on Message` que usaremos para recibir los mensajes enviados a nuestro bot de Telegram, necesita soporte SSL y como n8n estará ejecutándose en nuestro entorno local, utilizaremos **ngrok** para crear un dominio público accesible desde internet, exponiendo el puerto donde se encuentra ejecutando n8n.


### 1. Requisitos previos

Antes de continuar, es necesario tener instalado **n8n usando Docker Compose**, para esto podemos seguir la [guía oficial](https://docs.n8n.io/hosting/installation/server-setups/docker-compose/#4-create-an-env-file)

Si seguiste ese proceso, ya deberías contar con un directorio que incluya:

- un archivo `.yml`
- un archivo `.env`

También necesitás tener instalado [ngrok](https://ngrok.com/download).

---


### 2. Configurar ngrok y actualizar el archivo `.env`

1. Iniciá sesión en tu cuenta de ngrok.
2. Desde el *dashboard*, ingresá a la sección **Domains**.
3. Allí verás un dominio asignado automáticamente, por ejemplo:

   ```
   expellable-evonne-stylitic.ngrok-free.dev
   ```

4. Hacé clic sobre el dominio y copiá **solo el subdominio** (la parte antes del primer punto), por ejemplo:

   ```
   expellable-evonne-stylitic
   ```

5. Reemplazá los valores de `SUBDOMAIN` y `DOMAIN_NAME` en tu archivo `.env` de la siguiente forma:

```env
# DOMAIN_NAME and SUBDOMAIN together determine where n8n will be reachable from
# The top level domain to serve from
DOMAIN_NAME=ngrok-free.dev

# The subdomain to serve from
SUBDOMAIN=expellable-evonne-stylitic

# Optional timezone to set which gets used by Cron and other scheduling nodes
GENERIC_TIMEZONE=America/Argentina/Buenos_Aires

# The email address to use for the TLS/SSL certificate creation
SSL_EMAIL=user@example.com
```

---

Una vez modificado este archivo, debemos reiniciar los contenedores para aplicar los cambios:

```
docker compose down
docker compose up -d
```

---
### 3. Crear el nodo Trigger de Telegram (`on Message`)

1. Abrí n8n.
2. En el panel de nodos, buscá **Telegram**.
3. Seleccioná el nodo **on Message**.

Al abrirse la configuración del nodo, en la sección **Webhook URLs** deberías ver el dominio que configuraste en el archivo `.env` (el dominio de ngrok).

---


### 4. Crear las credenciales de Telegram

Para que el nodo pueda recibir los mensajes del bot:

1. Hacé clic en "Create New" dentro del apartado de credenciales.
2. Pegá el **Access Token** del bot. (Debe solicitarse previamente.)

---

### 5. Probar la recepción de mensajes

1. En el nodo `on Message`, hacé clic en **Execute Step**.
2. Enviá un mensaje al bot en Telegram:
   👉 https://t.me/FAMAFBot
3. Deberías ver los datos del mensaje aparecer dentro de n8n, como en la siguiente imagen:

<img width="1338" height="662" alt="image" src="https://github.com/user-attachments/assets/ff8d19e7-aa58-400d-9bde-e94f7fb2baca" />

Esto confirma que el webhook está correctamente configurado y que n8n puede recibir mensajes del bot desde un entorno local utilizando ngrok.

---

