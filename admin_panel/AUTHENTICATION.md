# Autenticación con FastAPI Users

Este proyecto ahora incluye registro de usuarios y autenticación usando la librería FastAPI Users.

## Instalación

Instala las nuevas dependencias:

```bash
pip install -r requirements.txt
```

## Variables de Entorno

Agrega lo siguiente a tu archivo `.env`:

```env
SECRET_KEY=tu-clave-secreta-aqui-minimo-32-caracteres
```

Puedes generar una clave secreta segura con:

```bash
openssl rand -hex 32
```

## Endpoints de la API

### Endpoints de Autenticación

#### Registrar un Nuevo Usuario
- **POST** `/auth/register`
- **Body**:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "ContraseñaSegura123!",
  "full_name": "Juan Pérez"
}
```
- **Respuesta**: Objeto de usuario

#### Iniciar Sesión
- **POST** `/auth/jwt/login`
- **Datos del Formulario**:
  - `username`: usuario@ejemplo.com (correo electrónico)
  - `password`: ContraseñaSegura123!
- **Respuesta**:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Cerrar Sesión
- **POST** `/auth/jwt/logout`
- **Cookies**: Se elimina automáticamente
- **Respuesta**: Mensaje de éxito

### Endpoints de Gestión de Usuarios

#### Obtener Usuario Actual
- **GET** `/auth/users/me`
- **Cookies**: Cookie de sesión automática
- **Respuesta**: Objeto del usuario actual

#### Actualizar Usuario Actual
- **PATCH** `/auth/users/me`
- **Cookies**: Cookie de sesión automática
- **Body**:
```json
{
  "email": "nuevocorreo@ejemplo.com",
  "full_name": "Nombre Actualizado",
  "password": "NuevaContraseña123!"
}
```

#### Eliminar Usuario Actual
- **DELETE** `/auth/users/me`
- **Cookies**: Cookie de sesión automática

### Endpoints de Recuperación de Contraseña

#### Solicitar Recuperación de Contraseña
- **POST** `/auth/reset-password/forgot-password`
- **Body**:
```json
{
  "email": "usuario@ejemplo.com"
}
```

#### Restablecer Contraseña
- **POST** `/auth/reset-password/reset-password`
- **Body**:
```json
{
  "token": "token-recuperacion-del-correo",
  "password": "NuevaContraseña123!"
}
```

### Endpoints de Verificación de Correo

#### Solicitar Verificación
- **POST** `/auth/verify/request-verify-token`
- **Body**:
```json
{
  "email": "usuario@ejemplo.com"
}
```

#### Verificar Correo Electrónico
- **POST** `/auth/verify/verify`
- **Body**:
```json
{
  "token": "token-verificacion"
}
```

## Proteger Rutas

Para proteger tus rutas y requerir autenticación, usa las dependencias de `app.auth`:

```python
from fastapi import APIRouter, Depends
from app.auth import current_active_user
from app.models.users import User

router = APIRouter()

@router.get("/ruta-protegida")
async def ruta_protegida(user: User = Depends(current_active_user)):
    return {"message": f"¡Hola {user.email}!"}
```

## Pruebas con cURL

### Registrar un usuario:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "prueba@ejemplo.com",
    "password": "ContraseñaSegura123!",
    "full_name": "Usuario Prueba"
  }'
```

### Iniciar sesión:
```bash
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=prueba@ejemplo.com&password=ContraseñaSegura123!"
```

### Acceder a ruta protegida:
```bash
curl -X GET "http://localhost:8000/auth/users/me" \
  -H "Cookie: adminuserauth=TU_TOKEN"
```

## Modelo de Usuario

El modelo de Usuario incluye:
- `id`: Identificador único del usuario (str)
- `email`: Correo electrónico del usuario (único)
- `hashed_password`: Contraseña hasheada de forma segura
- `is_active`: Si el usuario está activo (por defecto: verdadero)
- `is_verified`: Si el correo del usuario está verificado (por defecto: falso)
- `full_name`: Nombre completo opcional del usuario

## Arquitectura

- **Models**: `app/models/users.py` - Modelo de documento de usuario usando Beanie
- **Schemas**: `app/schemas/users.py` - Esquemas Pydantic para validación de datos de usuario
- **Auth**: `app/auth.py` - Configuración de autenticación y gestor de usuarios
- **Router**: `app/routers/auth.py` - Rutas de autenticación y gestión de usuarios
- **Database**: `app/database.py` - Inicialización de la base de datos incluyendo configuración de Beanie

## Características de Seguridad

- Autenticación basada en JWT
- Hashing de contraseñas usando bcrypt
- Transporte de Tokens usando Cookies
- Gestión de sesiones de usuario

## Notas

- Los tokens JWT expiran después de `ACCESS_TOKEN_EXPIRES_IN` segundos (configurado en settings)
- Las cookies son HTTP-only (solo para desarrollo) y se gestionan automáticamente
- Todas las contraseñas se hashean usando bcrypt antes de almacenarse
- La `SECRET_KEY` debe mantenerse segura y nunca ser comprometida en el control de versiones
- La autenticación ahora utiliza cookies en lugar de tokens Bearer en los encabezados
