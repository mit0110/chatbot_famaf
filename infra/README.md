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
# N8N - Dominio para acceso externo (ngrok)
# ============================================================
DOMAIN_NAME=ngrok-free.dev
SUBDOMAIN=tu-subdominio-ngrok

# ============================================================
# General
# ============================================================
GENERIC_TIMEZONE=America/Argentina/Buenos_Aires
SSL_EMAIL=tu-email@ejemplo.com

# ============================================================
# Langfuse - Claves API (se generan en Langfuse)
# ============================================================
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxx

# Langfuse Auth (importante para que funcione el login)
NEXTAUTH_SECRET=una-clave-secreta-segura
NEXTAUTH_URL=http://localhost:3000

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

| Variable      | Descripción                                                               |
| ------------- | ------------------------------------------------------------------------- |
| `DOMAIN_NAME` | Dominio base para n8n (ej: `ngrok-free.dev`)                              |
| `SUBDOMAIN`   | Subdominio asignado por ngrok para tu instancia                           |
| `SSL_EMAIL`   | Email para generar certificados SSL con Let's Encrypt (usado por Traefik) |

#### General

| Variable                      | Descripción                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------ |
| `GENERIC_TIMEZONE`            | Zona horaria para n8n y otros servicios (ej: `America/Argentina/Buenos_Aires`) |
| `NODE_FUNCTION_ALLOW_BUILTIN` | Módulos de Node.js permitidos en n8n (ej: `crypto`)                            |

#### Langfuse

| Variable              | Descripción                                                                                                                   |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `LANGFUSE_SECRET_KEY` | Clave secreta de tu proyecto en Langfuse (se genera en la UI de Langfuse)                                                     |
| `LANGFUSE_PUBLIC_KEY` | Clave pública de tu proyecto en Langfuse                                                                                      |
| `NEXTAUTH_SECRET`     | Clave secreta para encriptar sesiones de login. **Importante:** usar un valor fijo para evitar errores de sesión al reiniciar |
| `NEXTAUTH_URL`        | URL donde corre Langfuse (para redirecciones de auth)                                                                         |

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

## Configurar n8n con ngrok (acceso externo)

Para exponer n8n a internet usando ngrok:

### 1. Modificar compose.yml

Descomentar las líneas de configuración para ngrok en el servicio `n8n`:

```yaml
environment:
  # Comentar estas líneas (localhost):
  # - N8N_HOST=localhost
  # - N8N_PROTOCOL=http
  # - WEBHOOK_URL=http://localhost:5678/

  # Descomentar estas líneas (ngrok):
  - N8N_HOST=${SUBDOMAIN}.${DOMAIN_NAME}
  - N8N_PROTOCOL=https
  - WEBHOOK_URL=https://${SUBDOMAIN}.${DOMAIN_NAME}/
```

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

# Expone tu puerto al dominio obtenido en n8n
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
