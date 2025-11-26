# Game Distribution API Documentation

## Overview
Backend API for the game file distribution platform. Built with FastAPI and SQLite.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### Health Check

#### `GET /ping`
Keep-alive endpoint to prevent server spin-down.

**Authentication:** Not required

**Response:**
```json
{
  "status": "alive"
}
```

---

### Authentication

#### `POST /api/login`
Authenticate a user and receive a JWT token.

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_verified": true
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
```json
{
  "detail": "Invalid email or password"
}
```
- `401 Unauthorized` - Account not verified
```json
{
  "detail": "Account not verified"
}
```

---

### User Management

#### `POST /api/register`
Create a new user account. Requires authentication (intended for existing users to register new accounts).

**Authentication:** Required

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "securepassword"
}
```

**Success Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 2,
    "email": "newuser@example.com",
    "is_verified": false
  }
}
```

**Error Responses:**
- `400 Bad Request` - User already exists
```json
{
  "detail": "User with this email already exists"
}
```
- `401 Unauthorized` - Invalid or missing token
```json
{
  "detail": "Authorization header required"
}
```

---

#### `GET /api/users`
Get a list of all users.

**Authentication:** Required

**Response (200):**
```json
{
  "users": [
    {
      "id": 1,
      "email": "user1@example.com",
      "password_hash": "...",
      "is_verified": true
    },
    {
      "id": 2,
      "email": "user2@example.com",
      "password_hash": "...",
      "is_verified": false
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/users/{id}`
Get a specific user by ID.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - User ID

**Success Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "password_hash": "...",
  "is_verified": true
}
```

**Error Responses:**
- `404 Not Found` - User doesn't exist
```json
{
  "detail": "User not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/me`
Get the currently authenticated user's information.

**Authentication:** Required

**Success Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_verified": true
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `PUT /api/users/{id}`
Update a user's email and verification status.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - User ID

**Request Body:**
```json
{
  "email": "updated@example.com",
  "is_verified": true
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "email": "updated@example.com",
  "password_hash": "...",
  "is_verified": true
}
```

**Error Responses:**
- `404 Not Found` - User doesn't exist
```json
{
  "detail": "User not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

#### `DELETE /api/users/{id}`
Delete a user by ID.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - User ID

**Success Response (200):**
```json
{
  "message": "User deleted"
}
```

**Error Responses:**
- `404 Not Found` - User doesn't exist
```json
{
  "detail": "User not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK` - Successful request
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication failed or missing
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error (automatically handled by FastAPI)

Error responses follow this format:
```json
{
  "detail": "Error message description"
}
```

---

## Usage Example

### Login and Access Protected Route

```javascript
// 1. Login
const loginResponse = await fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const { token } = await loginResponse.json();

// 2. Use token to access protected route
const usersResponse = await fetch('http://localhost:8000/api/users', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const users = await usersResponse.json();
```

---

## Setup

### Requirements
- Python 3.8+
- FastAPI
- bcrypt
- PyJWT
- uvicorn

### Installation
```bash
pip install -r requirements.txt
```

### Running the Server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

---

## Notes

- All new users are created with `is_verified: false` by default
- Only verified users can log in
- The `/register` endpoint requires authentication to prevent unauthorized account creation
- Passwords are hashed using bcrypt before storage
- JWT tokens contain `user_id` and `email` in the payload