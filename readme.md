# Game Recommendation App - Work in progress

A backend API for managing and cataloging video games across multiple franchises and gaming systems. Built with FastAPI, SQLite, and designed to integrate with AI-powered recommendation features. 

## Project Overview

This API provides a comprehensive system for organizing video games by franchise and platform, with user authentication and full CRUD operations. The project demonstrates modern backend development practices including RESTful API design, JWT authentication, and relational database management.

## Features

- **User Authentication**: Secure JWT-based authentication with bcrypt password hashing
- **Game Catalog Management**: Full CRUD operations for games, franchises, and systems
- **Relational Database Design**: Properly normalized SQLite database with foreign key relationships
- **RESTful API**: Clean, well-documented endpoints following REST principles
- **Input Validation**: Pydantic models for request/response validation
- **AI Integration Ready**: Architecture designed to integrate with multi-agent AI recommendation system (Gemini + Groq)

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite3
- **Authentication**: JWT (PyJWT) + bcrypt
- **Validation**: Pydantic
- **Server**: Uvicorn
- **Future Integration**: Google Gemini API, Groq API

## Database Schema

### Users
- User authentication and authorization
- Email-based accounts with verification status

### Systems
- Gaming platforms (Nintendo 64, PlayStation, etc.)
- System images and metadata

### Franchises
- Game series/franchises (Mario, Zelda, etc.)
- Associated with specific systems
- Franchise branding images

### Games
- Individual game entries
- Linked to franchises and systems
- Game images and descriptions

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/JonLindholm11/Project-Evangelion.git
cd Project-Evangelion
```

2. Create and activate virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
python db/schema.py
```

5. (Optional) Seed with sample data
```bash
python seed.py
```

6. Run the server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Or see the detailed [API Documentation](API.md)

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Quick Start Authentication

1. Register a user (requires existing authenticated user)
2. Verify the user in the database
3. Login to receive JWT token
4. Use token for subsequent requests

## Example Usage
```javascript
// Login
const response = await fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const { token } = await response.json();

// Get all games
const games = await fetch('http://localhost:8000/api/games', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

## Project Structure
```
Project-Evangelion/Backend
├── db/
│   ├── client.py          # Database connection utilities
│   ├── schema.py          # Database schema definition
│   └── functions/         # Database CRUD functions
├── routes/
│   ├── users.py          # User endpoints
│   ├── systems.py        # System endpoints
│   ├── franchises.py     # Franchise endpoints
│   └── games.py          # Game endpoints
├── seed_data/            # JSON files for database seeding
├── main.py               # FastAPI application entry point
├── seed.py               # Database seeding script
└── requirements.txt      # Python dependencies
```

## Planned Features

- **AI-Powered Recommendations**: Multi-agent system using Gemini for natural language processing and Groq for intelligent database queries
- **Semantic Search**: Find games based on natural language descriptions
- **Personalized Suggestions**: Recommendations based on user preferences and play history
- **Store Integration**: Links to legitimate game retailers

## Development

### Running Tests
```bash
# Tests coming soon
pytest
```

### Database Reset
```bash
python db/schema.py  # Recreates tables
python seed.py       # Repopulates with sample data
```

## API Endpoints Summary

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - Create new user

### Users
- `GET /api/users` - List all users
- `GET /api/users/{id}` - Get specific user
- `GET /api/me` - Get current user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Systems
- Full CRUD operations for gaming platforms

### Franchises
- Full CRUD operations for game franchises

### Games
- Full CRUD operations for game catalog
- `GET /api/games/franchise/{franchise_id}` - Filter by franchise

## Contributing

This is a personal portfolio project, but feedback and suggestions are welcome!

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Jon Lindholm**
- GitHub: [@JonLindholm11](https://github.com/JonLindholm11)

## Acknowledgments

- FastAPI for the excellent framework and documentation
- The open-source community

---
