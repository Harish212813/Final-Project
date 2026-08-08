# FastAPI Calculator - Final Project

## Overview

This project is a full-stack FastAPI calculator application developed throughout the course. It includes secure user registration and login, JWT authentication, PostgreSQL database integration, complete BREAD functionality for calculations, automated testing, Docker containerization, and GitHub Actions for CI/CD.

For the final project, I expanded the calculator by adding two new calculation types: Power and Modulus. These operations are integrated into the backend, validation schemas, calculation factory, front-end dashboard, and automated tests.

Users can register, log in, and manage their own calculations through the front-end dashboard. Each calculation is connected to the logged-in user, so users can only access their own calculation history.

## Final Project Feature

The advanced feature added for the final project is support for two additional calculation operations:

- Power
- Modulus

### Power

The Power operation raises the first number to the power of the second number.

Example:

```text
2 ^ 3 = 8
```

### Modulus

The Modulus operation returns the remainder after dividing the first number by the second number.

Example:

```text
10 % 3 = 1
```

The application also validates modulus operations to prevent modulus by zero.

Both operations are available from the calculation dashboard and are saved to the user's calculation history like the original operations.

## Features

### User Authentication

- User registration
- User login
- Password hashing with bcrypt
- JWT access tokens
- Protected calculation routes
- User-specific calculation records
- Unauthorized-access handling
- Logout functionality

### Calculator Operations

The application supports:

- Add
- Subtract
- Multiply
- Divide
- Power
- Modulus
- Division-by-zero validation
- Modulus-by-zero validation

### BREAD Functionality

The application provides complete BREAD functionality for calculations:

- Browse all calculations belonging to the logged-in user
- Read the details of a specific calculation
- Edit an existing calculation
- Add a new calculation
- Delete a calculation

### Front-End

The application includes:

- Registration page
- Login page
- Calculation dashboard
- Create calculation form
- View calculation functionality
- Edit calculation functionality
- Delete calculation functionality
- Add, Subtract, Multiply, Divide, Power, and Modulus options
- Client-side numeric validation
- Division-by-zero validation
- Modulus-by-zero validation
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
- Trivy

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
├── test_e2e.py
├── test_main.py
├── test_operations.py
├── test_schemas.py
├── test_security.py
├── test_user_routes.py
└── test_users.py

.github/
└── workflows/
    └── tests.yml
```

## Clone the Repository

Clone the Final Project repository:

```bash
git clone https://github.com/Harish212813/Final-Project.git
cd Final-Project
```

## Create a Virtual Environment

Create a Python virtual environment:

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

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright Chromium browser:

```bash
playwright install chromium
```

## Run the Application Locally

Make sure PostgreSQL is running and the `DATABASE_URL` environment variable is configured.

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The application can then be accessed at:

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

Swagger API documentation:

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

## Testing

The project contains unit, integration, and end-to-end tests.

Run the complete test suite:

```bash
pytest
```

The completed final project currently has:

```text
76 passed
```

### Unit Tests

Unit tests verify individual application logic including:

- Add
- Subtract
- Multiply
- Divide
- Power
- Modulus
- Division-by-zero handling
- Modulus-by-zero handling
- Calculation factory behavior
- Pydantic validation
- Password security

Run operation tests with:

```bash
pytest tests/test_operations.py -v
```

### Integration Tests

Integration tests verify the FastAPI routes and database interactions, including:

- User registration
- User login
- Creating calculations
- Browsing calculations
- Reading calculations
- Editing calculations
- Deleting calculations
- Power calculations
- Modulus calculations
- Calculation history
- User ownership and authorization
- Invalid calculation requests

Run calculation route tests with:

```bash
pytest tests/test_calculation_routes.py -v
```

### End-to-End Tests

Playwright tests verify the application from the user's perspective through the front-end.

Run the E2E tests with:

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
- Power calculations
- Modulus calculations
- Division-by-zero validation
- Modulus-by-zero validation
- Unauthorized dashboard access
- Logout

## Docker Hub

The final project Docker image is available at:

```text
https://hub.docker.com/r/akhil212813/fastapi-calculator-final
```

Pull the latest Docker image with:

```bash
docker pull akhil212813/fastapi-calculator-final:latest
```

## GitHub Repository

The final project source code is available at:

```text
https://github.com/Harish212813/Final-Project
```

## CI/CD

GitHub Actions is used to automatically test, build, scan, and deploy the application.

When code is pushed to the `main` branch, the workflow:

1. Starts a PostgreSQL service.
2. Installs the Python dependencies.
3. Installs Playwright and Chromium.
4. Creates the database tables.
5. Starts the FastAPI server.
6. Runs the automated test suite.
7. Builds the Docker image.
8. Scans the Docker image with Trivy.
9. Logs in to Docker Hub using GitHub repository secrets.
10. Pushes the final Docker image to Docker Hub.

The Docker image is only pushed after the testing job completes successfully.

## Security

The application includes several security features:

- Passwords are hashed instead of stored as plain text
- JWT authentication
- Protected calculation endpoints
- User ownership checks
- Pydantic server-side validation
- Client-side form validation
- Invalid-token handling
- Unauthorized-access handling
- Docker Hub credentials stored using GitHub Actions secrets

## Final Project Summary

For the final project, I extended the existing FastAPI calculator by adding Power and Modulus operations. The new operations were added across the backend calculation logic, Pydantic validation, calculation factory, front-end interface, and automated tests.

The project maintains the existing secure JWT authentication and complete calculation BREAD functionality. Unit, integration, and Playwright E2E tests verify both the existing application and the new final-project functionality.

The application is containerized with Docker and uses GitHub Actions to automatically test, build, scan, and push the final image to Docker Hub.

## Author

Akhil B.