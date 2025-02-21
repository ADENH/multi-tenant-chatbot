
---

# Multi-Tenant Chatbot with OpenAI and FastAPI

![License](https://img.shields.io/badge/license-MIT-blue.svg) 

![Python](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10-blue) 

![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)

This repository contains a **multi-tenant chatbot** built using **FastAPI**, **OpenAI's GPT models**, and **PostgreSQL**. The chatbot supports multiple tenants, authenticates users via JWT tokens, and integrates with OpenAI's Chat Completion API for generating AI-driven responses.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Rate Limiting](#rate-limiting)
8. [Contributing](#contributing)
9. [License](#license)

---

## Features

- **Multi-Tenancy**: Supports multiple tenants with unique IDs.
- **Authentication**: Secure user authentication using JWT tokens.
- **AI-Powered Responses**: Integrates with OpenAI's Chat Completion API for generating intelligent responses.
- **Rate Limiting**: Prevents abuse with per-user rate limiting using `slowapi`.
- **Scalable Architecture**: Built with FastAPI for high performance and scalability.
- **Database Integration**: Uses PostgreSQL for storing user data and tenant information.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL database
- OpenAI API key (sign up at [OpenAI](https://platform.openai.com/))
- A `.env` file with configuration variables (see [Configuration](#configuration))

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/multi-tenant-openai-chatbot.git
   cd multi-tenant-openai-chatbot
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   - Create a PostgreSQL database.
   - Update the `.env` file with your database connection string.

5. **Run Migrations**
   If using Alembic for migrations:
   ```bash
   alembic upgrade head
   ```

6. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key-for-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Usage

### Register a User
Register a new user with a username, password, and tenant ID:
```bash
curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "securepassword123", "tenant_id": "tenant_1"}'
```

### Log In to Get a Token
Log in to receive a JWT token:
```bash
curl -X POST "http://127.0.0.1:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=securepassword123"
```

Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Send a Chat Message
Use the token to send a chat message:
```bash
curl --location 'http://127.0.0.1:8000/chat' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{"message": "What is your product?"}'
```

Response:
```json
{
    "response": "Our product is an AI-powered chatbot designed to assist users."
}
```

---

## API Endpoints

| Endpoint       | Method | Description                          | Requires Authentication |
|----------------|--------|--------------------------------------|-------------------------|
| `/register`    | POST   | Register a new user                  | No                      |
| `/token`       | POST   | Authenticate a user and get a token  | No                      |
| `/chat`        | POST   | Send a chat message and get a response | Yes (JWT token)       |

---

## Rate Limiting

The `/chat` endpoint enforces rate limiting to prevent abuse:
- **Limit**: 5 requests per minute per user.
- If the limit is exceeded, the server responds with:
  ```json
  {
      "detail": "Rate limit exceeded",
      "status_code": 429
  }
  ```

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.
- [OpenAI](https://platform.openai.com/) for the AI model integration.
- [SlowAPI](https://github.com/laurentS/slowapi) for rate limiting.

---

Feel free to customize this `README.md` further based on your project's specific needs. Let me know if you need help with anything else!