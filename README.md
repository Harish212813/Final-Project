# FastAPI Calculator

## Overview

This project is a FastAPI calculator application that has been built throughout the course. It includes calculator endpoints, PostgreSQL database integration, secure user authentication with JWT, client-side login and registration pages, automated testing, Docker support, and GitHub Actions for CI/CD.

## Features

- Basic calculator operations
  - Add
  - Subtract
  - Multiply
  - Divide
- FastAPI REST API
- PostgreSQL database with SQLAlchemy
- User registration and login
- Password hashing using bcrypt
- JWT authentication
- Client-side validation for registration and login
- Calculation CRUD (Browse, Read, Edit, Add, Delete)
- Pydantic request and response validation
- Unit, integration, and Playwright end-to-end tests
- Docker and Docker Compose support
- GitHub Actions CI/CD pipeline

## Technologies Used

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Passlib (bcrypt)
- Python-JOSE (JWT)
- Playwright
- Pytest
- Docker
- GitHub Actions

## Installation

Clone the repository:

```bash
git clone https://github.com/Harish212813/FastAPI-Calculator.git
cd FastAPI-Calculator
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the application:

```bash
uvicorn app.main:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test the API endpoints.

The registration and login pages are available at:

```
http://127.0.0.1:8000/register-page
```

```
http://127.0.0.1:8000/login-page
```

## Running Tests

Run all tests:

```bash
pytest
```

Run only Playwright tests:

```bash
pytest tests/e2e/test_auth.py --headed
```

## Docker

Build the Docker image:

```bash
docker compose up --build
```

The application, PostgreSQL database, and pgAdmin will start using Docker Compose.

## Project Structure

```
app/
├── main.py
├── models.py
├── schemas.py
├── security.py
├── database.py
├── services/
└── static/

tests/
├── test_main.py
├── test_users.py
├── test_security.py
├── test_schemas.py
├── test_calculation_model.py
├── test_calculation_factory.py
├── test_calculation_schemas.py
├── test_calculations.py
└── e2e/
    └── test_auth.py
```

## CI/CD

GitHub Actions automatically:

- Runs all unit, integration, and Playwright tests
- Builds the Docker image
- Pushes the Docker image to Docker Hub after successful tests

