# Admin Panel (FastAPI + MongoDB)

Este servicio levanta una aplicación web construida con FastAPI y una
base de datos MongoDB utilizando Docker Compose.

------------------------------------------------------------------------

## Configuración inicial (PRIMERO)

Antes de levantar los contenedores, es necesario configurar las
variables de entorno.

### 1) Crear el archivo `.env`

Copiá el archivo de ejemplo:

``` bash
cp .env_example .env
```

Luego abrí `.env` y ajustá las variables según tu entorno.

### Variables principales

-   `MONGO_INITDB_ROOT_USERNAME`\
    Usuario administrador que se crea al iniciar MongoDB.

-   `MONGO_INITDB_ROOT_PASSWORD`\
    Contraseña del usuario administrador.

-   `MONGO_INITDB_DATABASE`\
    Base de datos inicial que crea MongoDB.

-   `DATABASE_URL`\
    Cadena de conexión que usa la app para conectarse a MongoDB.

-   `CLIENT_ORIGIN`\
    Origen permitido para CORS (URL del frontend si aplica).

### Ejemplo de `DATABASE_URL`

``` bash
mongodb://<usuario>:<password>@mongo:27017/<database>?authSource=admin
```

Para una prueba inicial podés usar los valores por defecto, pero se
recomienda elegir una contraseña más segura.

------------------------------------------------------------------------

## Levantar el servicio con Docker

### 2) Instalar Docker y Docker Compose

Asegurate de tener Docker y Docker Compose instalados.

### 3) Primera vez (obligatorio)

La primera vez que levantes el proyecto es necesario construir la imagen
para instalar todas las dependencias:

``` bash
docker compose up --build
```

Esto construye la imagen, instala dependencias, crea los contenedores y
levanta la aplicación.

### 4) Siguientes ejecuciones

Una vez construida la imagen, podés iniciar el servicio en segundo plano
con:

``` bash
docker compose up -d
```

Solo será necesario volver a usar `--build` si:

-   Modificás el `Dockerfile`
-   Agregás nuevas dependencias
-   Cambiás algo que afecte la construcción de la imagen

------------------------------------------------------------------------

## Acceso a la aplicación

Una vez levantado el servicio:

-   App:\
    http://localhost:8000

-   Documentación Swagger:\
    http://localhost:8000/docs

-   Documentación ReDoc:\
    http://localhost:8000/redoc

------------------------------------------------------------------------

## Puertos utilizados

| Servicio | Puerto local | Puerto contenedor |
|----------|--------------|-------------------|
| FastAPI  | 8000         | 8000              |
| MongoDB  | 6000         | 27017             |

------------------------------------------------------------------------

## Detener el servicio

### Detener sin borrar datos

``` bash
docker compose stop
```

### Detener y eliminar contenedores (conservar datos)

``` bash
docker compose down
```

------------------------------------------------------------------------

## Borrar la base de datos (IMPORTANTE)

Si querés eliminar completamente la base de datos (incluye todos los
datos):

``` bash
docker compose down -v
```

Esto elimina el volumen de MongoDB y los datos no se pueden recuperar.

------------------------------------------------------------------------

## Acceder a MongoDB desde Docker

Podés abrir la consola de MongoDB:

``` bash
docker compose exec mongo mongosh -u <usuario> -p <password> --authenticationDatabase admin
```

Usá el usuario y contraseña definidos en el `.env`.

------------------------------------------------------------------------

## Opcional: Exponer con ngrok (por ejemplo para n8n)

### 1) Configurar token (una sola vez)

``` bash
ngrok config add-authtoken <tu_token>
```

### 2) Exponer la app

``` bash
ngrok http 8000
```

ngrok va a mostrar una URL pública similar a:

https://xxxx.ngrok-free.app

Esa URL puede usarse desde servicios externos como n8n.

