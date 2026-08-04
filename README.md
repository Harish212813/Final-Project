# FastAPI Calculator

## Overview

This project is a full-stack FastAPI calculator application developed throughout the course. It includes secure user registration and login, JWT authentication, PostgreSQL database integration, complete BREAD functionality for calculations, automated testing, Docker containerization, and GitHub Actions for CI/CD.

Users can register, log in, and manage their own calculations through a front-end dashboard. Each calculation is connected to the logged-in user, so users can only access their own data.

## Features

### User Authentication

- User registration
- User login
- Password hashing with bcrypt
- JWT access tokens
- Protected calculation routes
- User-specific calculation records

### Calculator Operations

- Add
- Subtract
- Multiply
- Divide
- Division-by-zero validation

### BREAD Functionality

- Browse all calculations belonging to the logged-in user
- Read the details of one calculation
- Edit an existing calculation
- Add a new calculation
- Delete a calculation

### Front-End

- Registration page
- Login page
- Calculation dashboard
- Create, view, edit, and delete controls
- Client-side numeric validation
- Division-by-zero validation
- JWT token storage
- Logout functionality

## Technologies Used

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT
- Passlib
- bcrypt
- HTML
- CSS
- JavaScript
- Pytest
- Playwright
- Docker
- Docker Compose
- GitHub Actions

## Project Structure

```text
app/
├── database.py
├── main.py
├── models.py
├── operations.py
├── schemas.py
├── security.py
├── services/
│   └── calculation_factory.py
└── static/
    ├── calculations.html
    ├── calculations.js
    ├── login.html
    ├── login.js
    ├── register.html
    ├── register.js
    └── styles.css

tests/
├── e2e/
│   ├── test_auth.py
│   └── test_calculations.py
├── test_calculation_factory.py
├── test_calculation_model.py
├── test_calculation_routes.py
├── test_calculation_schemas.py
├── test_main.py
├── test_operations.py
├── test_schemas.py
├── test_security.py
├── test_user_routes.py
└── test_users.py
```

## Clone the Repository

```bash
git clone https://github.com/Harish212813/FastAPI-Calculator.git
cd FastAPI-Calculator
```

## Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on macOS or Linux:

```bash
source venv/bin/activate
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
playwright install chromium
```

## Run the Application Locally

Make sure PostgreSQL is running and the `DATABASE_URL` environment variable is configured.

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Open the application at:

```text
http://localhost:8000
```

Registration page:

```text
http://localhost:8000/register-page
```

Login page:

```text
http://localhost:8000/login-page
```

Calculation dashboard:

```text
http://localhost:8000/calculations-page
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Run with Docker

Build and start the application, PostgreSQL, and pgAdmin:

```bash
docker compose up --build -d
```

Check the running containers:

```bash
docker compose ps
```

The services are available at:

- FastAPI application: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- pgAdmin: `http://localhost:5050`

Stop the containers:

```bash
docker compose down
```

## Run Tests

Run the complete test suite:

```bash
pytest
```

The completed project currently includes 64 passing tests.

Run only the calculation route tests:

```bash
pytest tests/test_calculation_routes.py -v
```

Run the Playwright end-to-end tests:

```bash
pytest tests/e2e -v
```

The Playwright tests cover:

- User registration
- User login
- Invalid login
- Password mismatch
- Adding calculations
- Browsing calculations
- Reading calculations
- Editing calculations
- Deleting calculations
- Division-by-zero validation
- Unauthorized dashboard access
- Logout

## Docker Hub

The Docker image is available at:

```text
https://hub.docker.com/r/akhil212813/fastapi-calculator
```

Pull the image:

```bash
docker pull akhil212813/fastapi-calculator:latest
```

## GitHub Repository

```text
https://github.com/Harish212813/FastAPI-Calculator
```

## CI/CD

The GitHub Actions workflow is configured to support automated testing and Docker image builds. This helps confirm that the application continues to work correctly whenever changes are pushed to the repository.

## Security

The application includes:

- Hashed passwords instead of plain-text password storage
- JWT authentication
- Protected calculation endpoints
- User ownership checks
- Server-side validation with Pydantic
- Client-side form validation
- Unauthorized-access handling

## Author

Akhil B.