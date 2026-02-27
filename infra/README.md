# Infraestructura Chatbot FaMAF

Este directorio contiene la configuración de Docker Compose para levantar todos los servicios del proyecto.

## Servicios

| Servicio       | Descripción               | URL Local                                       |
| -------------- | ------------------------- | ----------------------------------------------- |
| **n8n**        | Workflow Automation       | http://localhost:5678                           |
| **Langfuse**   | LLM Observability         | http://localhost:3000                           |
| **FastAPI**    | Admin Panel               | http://localhost:8000                           |
| **MongoDB**    | Base de datos Admin Panel | localhost:6000                                  |
| **PostgreSQL** | Base de datos Langfuse    | localhost:5432                                  |
| **ClickHouse** | Analytics Langfuse        | localhost:8123                                  |
| **MinIO**      | Object Storage            | localhost:9090 (API) / localhost:9091 (Console) |
| **Redis**      | Cache Langfuse            | localhost:6379                                  |
| **Traefik**    | Reverse Proxy             | localhost:80 / localhost:443                    |

## Configuración

### Variables de entorno (.env)

Crear un archivo `.env` en este directorio con las siguientes variables:

```bash
# ============================================================
# N8N 
# ============================================================

# ------------------------------------------------------------
# MODO NGROK (usar cuando exponés con dominio público)
# ------------------------------------------------------------
# DOMAIN_NAME=ngrok-free.dev
# SUBDOMAIN=tu-subdominio-ngrok
# N8N_HOST=${SUBDOMAIN}.${DOMAIN_NAME}
# N8N_PROTOCOL=https
# WEBHOOK_URL=https://${SUBDOMAIN}.${DOMAIN_NAME}/

# ------------------------------------------------------------
# MODO LOCAL (usar cuando accedés desde http://localhost:5678)
# ------------------------------------------------------------
N8N_HOST=localhost
N8N_PROTOCOL=http
WEBHOOK_URL=http://n8n:5678/

# ============================================================
# General
# ============================================================
GENERIC_TIMEZONE=America/Argentina/Buenos_Aires
SSL_EMAIL=tu-email@ejemplo.com

# ============================================================
# Langfuse
# ============================================================

# Langfuse Autenticación y URL base
NEXTAUTH_SECRET=una-clave-secreta-segura
NEXTAUTH_URL=http://localhost:3000

# Langfuse - Usuario y proyecto inicial (se crean automáticamente)
LANGFUSE_INIT_ORG_ID=mi-org-id
LANGFUSE_INIT_ORG_NAME=FaMAF
LANGFUSE_INIT_PROJECT_ID=mi-proyecto-id
LANGFUSE_INIT_PROJECT_NAME=chatbot-famaf
LANGFUSE_INIT_USER_EMAIL=admin@famaf.unc.edu.ar
LANGFUSE_INIT_USER_NAME=Admin
LANGFUSE_INIT_USER_PASSWORD=Admin123!

# ============================================================
# MongoDB - Admin Panel
# ============================================================
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password123
MONGO_INITDB_DATABASE=fastapi
MONGO_DATABASE_URL=mongodb://admin:password123@mongo:27017/fastapi?authSource=admin

# ============================================================
# Config
# ============================================================
CLIENT_ORIGIN=*
NODE_FUNCTION_ALLOW_BUILTIN=crypto
```

### Descripción de variables

#### N8N y acceso externo

| Variable       | Descripción                                                  |
| -------------- | ------------------------------------------------------------ |
| `DOMAIN_NAME`  | Dominio base para n8n (ej: `ngrok-free.dev`)                 |
| `SUBDOMAIN`    | Subdominio asignado por ngrok para tu instancia              |
| `N8N_HOST`     | Host público donde se accede a n8n (ej: `subdominio.dominio.com` o `localhost`) |
| `N8N_PROTOCOL` | Protocolo usado por n8n (`http` para local, `https` cuando se expone públicamente) |
| `WEBHOOK_URL`  | URL pública base que n8n utiliza para generar webhooks (ej: `https://subdominio.dominio.com/`) |
| `SSL_EMAIL`    | Email para generar certificados SSL con Let's Encrypt (usado por Traefik) |

#### General

| Variable                      | Descripción                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------ |
| `GENERIC_TIMEZONE`            | Zona horaria para n8n y otros servicios (ej: `America/Argentina/Buenos_Aires`) |
| `NODE_FUNCTION_ALLOW_BUILTIN` | Módulos de Node.js permitidos en n8n (ej: `crypto`)                            |

#### Langfuse

| Variable                      | Descripción                                                                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `NEXTAUTH_SECRET`             | Clave secreta para encriptar sesiones de login. **Importante:** usar un valor fijo para evitar errores de sesión al reiniciar |
| `NEXTAUTH_URL`                | URL donde corre Langfuse (para redirecciones de auth)                                                                         |
| `LANGFUSE_INIT_ORG_ID`        | ID único de la organización inicial (requerido para activar la inicialización)                                                |
| `LANGFUSE_INIT_ORG_NAME`      | Nombre de la organización que se crea automáticamente al iniciar                                                              |
| `LANGFUSE_INIT_PROJECT_ID`    | ID único del proyecto inicial                                                                                                 |
| `LANGFUSE_INIT_PROJECT_NAME`  | Nombre del proyecto inicial                                                                                                   |
| `LANGFUSE_INIT_USER_EMAIL`    | Email del usuario administrador inicial                                                                                       |
| `LANGFUSE_INIT_USER_NAME`     | Nombre del usuario administrador inicial                                                                                      |
| `LANGFUSE_INIT_USER_PASSWORD` | Contraseña del usuario administrador inicial (debe incluir letras, números y caracteres especiales)                           |

##### 🔐 Generar un NEXTAUTH_SECRET seguro

Podés generar una clave segura con OpenSSL:

```bash
openssl rand -base64 32
```

#### MongoDB (Admin Panel)

| Variable                     | Descripción                                                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `MONGO_INITDB_ROOT_USERNAME` | Usuario administrador que se crea al iniciar MongoDB                                                                |
| `MONGO_INITDB_ROOT_PASSWORD` | Contraseña del usuario administrador                                                                                |
| `MONGO_INITDB_DATABASE`      | Base de datos inicial que crea MongoDB                                                                              |
| `MONGO_DATABASE_URL`         | Cadena de conexión que usa FastAPI para conectarse a MongoDB                                                        |
| `CLIENT_ORIGIN`              | Origen permitido para CORS (`*` permite todos, se puede restringir a la url donde accedas a n8n para mas seguridad) |

#### Formato de MONGO_DATABASE_URL

```
mongodb://<usuario>:<password>@mongo:27017/<database>?authSource=admin
```

> **Nota:** Para una prueba inicial podés usar los valores por defecto, pero se recomienda elegir contraseñas más seguras en producción.

## Uso

### Levantar todos los servicios

**Primera vez** (construye la imagen de FastAPI):

```bash
docker compose up -d --build
```

**Siguientes veces:**

```bash
docker compose up -d
```

> **Nota:** Usá `--build` cada vez que modifiques el código de FastAPI o su Dockerfile.

### Acceder a los servicios

Una vez levantados los contenedores, podés acceder a:

| Servicio        | URL                                                          | Descripción                     |
| --------------- | ------------------------------------------------------------ | ------------------------------- |
| **n8n**         | http://localhost:5678<br />  (o url de ngrok si estas utilizandolo) | Crear y gestionar workflows     |
| **Langfuse**    | http://localhost:3000                                        | Observabilidad de LLMs          |
| **Admin Panel** | http://localhost:8000/admin                                  | Panel de administración FastAPI |

### Links internos para n8n

Cuando configures credenciales o conexiones desde n8n hacia otros servicios (como Langfuse o FastAPI), usa las URLs internas de Docker:

- Para Langfuse: `http://langfuse-web:3000`
- Para FastAPI: `http://fastapi:8000`
- Para N8N: `http://n8n:5678` si estas corriendo local (o la URL de ngrok en caso de utilizar ngrok) 

Estas URLs permiten que n8n se comunique directamente con los servicios dentro de la red de Docker, evitando problemas de acceso o firewall. No uses las URLs externas (localhost) para conexiones internas entre contenedores.

Ejemplo: Al crear una credencial en n8n para Langfuse, usar `http://langfuse-web:3000` como host.

### Ver logs

```bash
# Todos los servicios
docker compose logs -f

# Un servicio específico
docker compose logs -f n8n
docker compose logs -f langfuse-web
```

### Detener servicios

```bash
docker compose down
```

### Reiniciar un servicio

```bash
docker compose restart n8n
```

## Configurar n8n con ngrok (acceso externo) o Local

Para exponer n8n a internet usando ngrok:

### 1. Modificar .env

Descomentar / comentar las variables según el modo de uso:

- ✅ **Modo local (desarrollo sin acceso externo)** → usar las variables por defecto (`localhost`)
- 🌍 **Modo externo con ngrok** → comentar las de `localhost` y descomentar las de `ngrok`

```yaml
# ------------------------------------------------------------
# MODO NGROK (usar cuando exponés con dominio público)
# ------------------------------------------------------------
# DOMAIN_NAME=ngrok-free.dev
# SUBDOMAIN=tu-subdominio-ngrok
# N8N_HOST=${SUBDOMAIN}.${DOMAIN_NAME}
# N8N_PROTOCOL=https
# WEBHOOK_URL=https://${SUBDOMAIN}.${DOMAIN_NAME}/

# ------------------------------------------------------------
# MODO LOCAL (usar cuando accedés desde http://localhost:5678)
# ------------------------------------------------------------
N8N_HOST=localhost
N8N_PROTOCOL=http
WEBHOOK_URL=http://n8n:5678/

```

⚠️ Es importante que `WEBHOOK_URL` coincida exactamente con la URL desde donde accedés a n8n. 

### 2. Configurar .env

Asegúrate de tener configurado tu dominio de ngrok:

```bash
DOMAIN_NAME=ngrok-free.dev
SUBDOMAIN=tu-subdominio-ngrok
```

### 3. Reiniciar n8n

```bash
docker compose restart n8n
```

### 4. Ejecutar ngrok

En una terminal separada:

```bash
# Asegurate de tener configurado ngrok con tu api_key (necesario solo la primera vez)
ngrok config add-authtoken <tu_token>

# Expone el puerto de n8n al dominio obtenido en ngrok
ngrok http 5678 --domain=tu-subdominio-ngrok.ngrok-free.dev

```

### 5. Acceder a n8n

Abrí en el navegador: `https://tu-subdominio-ngrok.ngrok-free.dev`

## Volúmenes

Los datos persistentes se guardan en los siguientes volúmenes Docker:

| Volumen                                  | Descripción                      |
| ---------------------------------------- | -------------------------------- |
| `chatbot_famaf_n8n_data`                 | Workflows y configuración de n8n |
| `chatbot_famaf_traefik_data`             | Certificados SSL de Traefik      |
| `chatbot_famaf_mongo`                    | Datos de MongoDB (Admin Panel)   |
| `chatbot_famaf_langfuse_postgres_data`   | Datos de PostgreSQL (Langfuse)   |
| `chatbot_famaf_langfuse_clickhouse_data` | Datos de ClickHouse (Langfuse)   |
| `chatbot_famaf_langfuse_minio_data`      | Archivos de MinIO (Langfuse)     |

## Troubleshooting

### n8n: Webhooks no funcionan

Verificá que `WEBHOOK_URL` coincida con la URL desde donde accedés a n8n.

### Puertos en uso

Si algún puerto está ocupado, podés modificar el mapeo en `compose.yml`. Por ejemplo, cambiar `3000:3000` a `3001:3000` para Langfuse.
