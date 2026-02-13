# Admin Panel (FastAPI + MongoDB)

Este servicio levanta una app web (FastAPI) y una base de datos (MongoDB) con Docker.

## Pasos

1) Instala Docker y Docker Compose.
2) Abre una terminal en esta carpeta.
3) Ejecuta:

```bash
docker compose up -d
```

Eso inicia todo.

Opcional (solo si cambiaste dependencias o el Dockerfile):

```bash
docker compose up --build
```

## Dónde abrir la app

- App: http://localhost:8000
- Documentación API (Swagger): http://localhost:8000/docs
- Documentación API (ReDoc): http://localhost:8000/redoc

## Puertos usados

- App (Uvicorn/FastAPI): `8000` en tu computadora -> `8000` dentro del contenedor
- MongoDB: `6000` en tu computadora -> `27017` dentro del contenedor

## Configurar .env

1) Copia el archivo de ejemplo:

```bash
cp .env_example .env
```

2) Abre `.env`. En este archivo podés modificar las variables.

Claves principales y para qué se usan:

- `MONGO_INITDB_ROOT_USERNAME`: usuario administrador que crea MongoDB al iniciar.
- `MONGO_INITDB_ROOT_PASSWORD`: contraseña del usuario administrador.
- `MONGO_INITDB_DATABASE`: nombre de la base de datos inicial que crea MongoDB.
- `DATABASE_URL`: cadena de conexión que usa la app para conectarse a MongoDB.
- `CLIENT_ORIGIN`: origen permitido para CORS (la URL del frontend si aplica).

Ejemplo de `DATABASE_URL`:

```bash
mongodb://<usuario>:<password>@mongo:27017/<database>?authSource=admin
```
Para una prueba inicial se pueden utilizar las variables tal como están, pero te recomendamos elegir una contraseña más fuerte para el administrador de tu base de datos.

## Detener el servicio (normal)

Para detener sin borrar datos:

```bash
docker compose stop
```

Para detener y eliminar los contenedores, pero conservar la base de datos:

```bash
docker compose down
```

## Borrar la base de datos (MUY IMPORTANTE)

Si querés borrar la base de datos, tenés que eliminar el volumen. Esto borra TODOS los datos y no se pueden recuperar.

```bash
docker compose down -v
```

## Acceder a MongoDB desde Docker

Podés acceder a la consola de MongoDB:

```bash
docker compose exec mongo mongosh -u <usuario> -p <password> --authenticationDatabase admin
```

Usa el usuario y password del `.env`.

