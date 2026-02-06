# FastAPI Users Authentication

This project now includes user registration and authentication using the FastAPI Users library.

## Installation

Install the new dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Add the following to your `.env` file if not already present:

```env
SECRET_KEY=your-secret-key-here-min-32-characters
```

You can generate a secure secret key with:

```bash
openssl rand -hex 32
```

## API Endpoints

### Authentication Endpoints

#### Register a New User
- **POST** `/auth/register`
- **Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```
- **Response**: User object

#### Login
- **POST** `/auth/jwt/login`
- **Form Data**:
  - `username`: user@example.com (email)
  - `password`: SecurePassword123!
- **Response**:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Logout
- **POST** `/auth/jwt/logout`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Success message

### User Management Endpoints

#### Get Current User
- **GET** `/auth/users/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Current user object

#### Update Current User
- **PATCH** `/auth/users/me`
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
```json
{
  "email": "newemail@example.com",
  "full_name": "Updated Name",
  "password": "NewPassword123!"
}
```

#### Delete Current User
- **DELETE** `/auth/users/me`
- **Headers**: `Authorization: Bearer <token>`

### Password Reset Endpoints

#### Request Password Reset
- **POST** `/auth/reset-password/forgot-password`
- **Body**:
```json
{
  "email": "user@example.com"
}
```

#### Reset Password
- **POST** `/auth/reset-password/reset-password`
- **Body**:
```json
{
  "token": "reset-token-from-email",
  "password": "NewPassword123!"
}
```

### Email Verification Endpoints

#### Request Verification
- **POST** `/auth/verify/request-verify-token`
- **Body**:
```json
{
  "email": "user@example.com"
}
```

#### Verify Email
- **POST** `/auth/verify/verify`
- **Body**:
```json
{
  "token": "verification-token"
}
```

## Protecting Routes

To protect your routes and require authentication, use the dependencies from `app.auth`:

```python
from fastapi import APIRouter, Depends
from app.auth import current_active_user
from app.models.users import User

router = APIRouter()

@router.get("/protected-route")
async def protected_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
```

For superuser-only routes:

```python
from app.auth import current_superuser

@router.get("/admin-only")
async def admin_route(user: User = Depends(current_superuser)):
    return {"message": "Admin access granted"}
```

## Testing with cURL

### Register a user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

### Login:
```bash
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=SecurePass123!"
```

### Access protected route:
```bash
curl -X GET "http://localhost:8000/auth/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## User Model

The User model includes:
- `id`: Unique user identifier (str)
- `email`: User's email address (unique)
- `hashed_password`: Securely hashed password
- `is_active`: Whether the user is active (default: true)
- `is_superuser`: Whether the user has superuser privileges (default: false)
- `is_verified`: Whether the user's email is verified (default: false)
- `full_name`: Optional full name of the user

## Architecture

- **Models**: `app/models/users.py` - User document model using Beanie
- **Schemas**: `app/schemas/users.py` - Pydantic schemas for user data validation
- **Auth**: `app/auth.py` - Authentication configuration and user manager
- **Router**: `app/routers/auth.py` - Authentication and user management routes
- **Database**: `app/database.py` - Database initialization including Beanie setup

## Security Features

- JWT-based authentication
- Password hashing using bcrypt
- Email verification support
- Password reset functionality
- Secure token generation
- User session management

## Notes

- The JWT tokens expire after `ACCESS_TOKEN_EXPIRES_IN` seconds (configured in settings)
- Email verification and password reset require email service configuration (currently logs tokens to console)
- All passwords are hashed using bcrypt before storage
- The SECRET_KEY should be kept secure and never committed to version control
