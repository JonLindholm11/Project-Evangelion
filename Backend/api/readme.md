# Game Recommendation API Documentation

## Overview
Backend API for the game recommendation platform. Built with FastAPI and SQLite.

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

### Systems Management

#### `POST /api/systems`
Create a new gaming system.

**Authentication:** Required

**Request Body:**
```json
{
  "system_name": "Nintendo 64",
  "system_img": "https://example.com/images/n64.png"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "system_name": "Nintendo 64",
  "system_img": "https://example.com/images/n64.png"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/systems`
Get a list of all gaming systems.

**Authentication:** Required

**Success Response (200):**
```json
{
  "systems": [
    {
      "id": 1,
      "system_name": "Nintendo 64",
      "system_img": "https://example.com/images/n64.png"
    },
    {
      "id": 2,
      "system_name": "PlayStation 1",
      "system_img": "https://example.com/images/ps1.png"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/systems/{id}`
Get a specific gaming system by ID.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - System ID

**Success Response (200):**
```json
{
  "id": 1,
  "system_name": "Nintendo 64",
  "system_img": "https://example.com/images/n64.png"
}
```

**Error Responses:**
- `404 Not Found` - System doesn't exist
```json
{
  "detail": "System not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

#### `PUT /api/systems/{id}`
Update a gaming system's information.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - System ID

**Request Body:**
```json
{
  "system_name": "Nintendo 64 Updated",
  "system_img": "https://example.com/images/n64-new.png"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "system_name": "Nintendo 64 Updated",
  "system_img": "https://example.com/images/n64-new.png"
}
```

**Error Responses:**
- `404 Not Found` - System doesn't exist
```json
{
  "detail": "System not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

#### `DELETE /api/systems/{id}`
Delete a gaming system by ID.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - System ID

**Success Response (200):**
```json
{
  "message": "System deleted"
}
```

**Error Responses:**
- `404 Not Found` - System doesn't exist
```json
{
  "detail": "System not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

### Games Management

#### `POST /api/games`
Create a new game entry.

**Authentication:** Required

**Request Body:**
```json
{
  "franchise_id": 1,
  "system_id": 1,
  "game_name": "Super Mario 64",
  "game_img": "https://example.com/images/mario64.png",
  "description": "A classic 3D platformer for Nintendo 64"
}
```

**Note:** `game_img` and `description` are optional fields.

**Success Response (200):**
```json
{
  "id": 1,
  "franchise_id": 1,
  "system_id": 1,
  "game_name": "Super Mario 64",
  "game_img": "https://example.com/images/mario64.png",
  "description": "A classic 3D platformer for Nintendo 64",
  "franchise_name": "Mario",
  "system_name": "Nintendo 64"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/games`
Get a list of all games with franchise and system information.

**Authentication:** Required

**Success Response (200):**
```json
{
  "games": [
    {
      "id": 1,
      "franchise_id": 1,
      "system_id": 1,
      "game_name": "Super Mario 64",
      "game_img": "https://example.com/images/mario64.png",
      "description": "A classic 3D platformer for Nintendo 64",
      "franchise_name": "Mario",
      "system_name": "Nintendo 64"
    },
    {
      "id": 2,
      "franchise_id": 2,
      "system_id": 1,
      "game_name": "The Legend of Zelda: Ocarina of Time",
      "game_img": "https://example.com/images/zelda-oot.png",
      "description": "Epic adventure game",
      "franchise_name": "The Legend of Zelda",
      "system_name": "Nintendo 64"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/games/{id}`
Get a specific game by ID with franchise and system information.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - Game ID

**Success Response (200):**
```json
{
  "id": 1,
  "franchise_id": 1,
  "system_id": 1,
  "game_name": "Super Mario 64",
  "game_img": "https://example.com/images/mario64.png",
  "description": "A classic 3D platformer for Nintendo 64",
  "franchise_name": "Mario",
  "system_name": "Nintendo 64"
}
```

**Error Responses:**
- `404 Not Found` - Game doesn't exist
```json
{
  "detail": "Game not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/games/franchise/{franchise_id}`
Get all games belonging to a specific franchise.

**Authentication:** Required

**URL Parameters:**
- `franchise_id` (integer) - Franchise ID

**Success Response (200):**
```json
{
  "games": [
    {
      "id": 1,
      "franchise_id": 1,
      "system_id": 1,
      "game_name": "Super Mario 64",
      "game_img": "https://example.com/images/mario64.png",
      "description": "A classic 3D platformer for Nintendo 64",
      "franchise_name": "Mario",
      "system_name": "Nintendo 64"
    },
    {
      "id": 5,
      "franchise_id": 1,
      "system_id": 3,
      "game_name": "Super Mario Sunshine",
      "game_img": "https://example.com/images/sunshine.png",
      "description": "Mario adventure on GameCube",
      "franchise_name": "Mario",
      "system_name": "GameCube"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `PUT /api/games/{id}`
Update a game's information.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - Game ID

**Request Body:**
```json
{
  "franchise_id": 1,
  "system_id": 1,
  "game_name": "Super Mario 64 Updated",
  "game_img": "https://example.com/images/mario64-new.png",
  "description": "Updated classic 3D platformer"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "franchise_id": 1,
  "system_id": 1,
  "game_name": "Super Mario 64 Updated",
  "game_img": "https://example.com/images/mario64-new.png",
  "description": "Updated classic 3D platformer",
  "franchise_name": "Mario",
  "system_name": "Nintendo 64"
}
```

**Error Responses:**
- `404 Not Found` - Game doesn't exist
```json
{
  "detail": "Game not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

#### `DELETE /api/games/{id}`
Delete a game by ID.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - Game ID

**Success Response (200):**
```json
{
  "message": "Game deleted"
}
```

**Error Responses:**
- `404 Not Found` - Game doesn't exist
```json
{
  "detail": "Game not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

### Franchises Management

#### `POST /api/franchises`
Create a new game franchise.

**Authentication:** Required

**Request Body:**
```json
{
  "system_id": 1,
  "franchise_name": "Mario",
  "franchise_img": "https://example.com/images/mario-franchise.png"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "system_id": 1,
  "franchise_name": "Mario",
  "franchise_img": "https://example.com/images/mario-franchise.png",
  "system_name": "Nintendo 64"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/franchises`
Get a list of all franchises with system information.

**Authentication:** Required

**Success Response (200):**
```json
{
  "franchises": [
    {
      "id": 1,
      "system_id": 1,
      "franchise_name": "Mario",
      "franchise_img": "https://example.com/images/mario-franchise.png",
      "system_name": "Nintendo 64"
    },
    {
      "id": 2,
      "system_id": 1,
      "franchise_name": "The Legend of Zelda",
      "franchise_img": "https://example.com/images/zelda-franchise.png",
      "system_name": "Nintendo 64"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

#### `GET /api/franchises/{id}`
Get a specific franchise by ID with system information.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - Franchise ID

**Success Response (200):**
```json
{
  "id": 1,
  "system_id": 1,
  "franchise_name": "Mario",
  "franchise_img": "https://example.com/images/mario-franchise.png",
  "system_name": "Nintendo 64"
}
```

**Error Responses:**
- `404 Not Found` - Franchise doesn't exist
```json
{
  "detail": "Franchise not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

#### `PUT /api/franchises/{id}`
Update a franchise's information.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - Franchise ID

**Request Body:**
```json
{
  "system_id": 1,
  "franchise_name": "Super Mario",
  "franchise_img": "https://example.com/images/mario-franchise-updated.png"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "system_id": 1,
  "franchise_name": "Super Mario",
  "franchise_img": "https://example.com/images/mario-franchise-updated.png",
  "system_name": "Nintendo 64"
}
```

**Error Responses:**
- `404 Not Found` - Franchise doesn't exist
```json
{
  "detail": "Franchise not found"
}
```
- `401 Unauthorized` - Invalid or missing token

---

#### `DELETE /api/franchises/{id}`
Delete a franchise by ID.

**Authentication:** Required

**URL Parameters:**
- `id` (integer) - Franchise ID

**Success Response (200):**
```json
{
  "message": "franchise deleted"
}
```

**Error Responses:**
- `404 Not Found` - Franchise doesn't exist
```json
{
  "detail": "Franchise not found"
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
pip install fastapi uvicorn bcrypt pyjwt --break-system-packages
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