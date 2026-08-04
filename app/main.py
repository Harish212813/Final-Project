import logging

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Calculation, User
from app.operations import add, divide, multiply, subtract
from app.schemas import (
    CalculationCreate,
    CalculationRead,
    CalculationUpdate,
    TokenResponse,
    UserCreate,
    UserEmailLogin,
    UserLogin,
    UserRead,
)
from app.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.services.calculation_factory import CalculationFactory


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


@app.get("/register-page", include_in_schema=False)
def register_page():
    return FileResponse("app/static/register.html")


@app.get("/login-page", include_in_schema=False)
def login_page():
    return FileResponse("app/static/login.html")

@app.get("/calculations-page", include_in_schema=False)
def calculations_page():
    return FileResponse("app/static/calculations.html")


@app.get("/")
def home():
    logger.info("Home endpoint was called")

    return {
        "message": "FastAPI Calculator is running"
    }


@app.get("/add")
def add_numbers(a: float, b: float):
    result = add(a, b)

    logger.info(
        f"Add operation: {a} + {b} = {result}"
    )

    return {
        "operation": "add",
        "result": result,
    }


@app.get("/subtract")
def subtract_numbers(a: float, b: float):
    result = subtract(a, b)

    logger.info(
        f"Subtract operation: {a} - {b} = {result}"
    )

    return {
        "operation": "subtract",
        "result": result,
    }


@app.get("/multiply")
def multiply_numbers(a: float, b: float):
    result = multiply(a, b)

    logger.info(
        f"Multiply operation: {a} * {b} = {result}"
    )

    return {
        "operation": "multiply",
        "result": result,
    }


@app.get("/divide")
def divide_numbers(a: float, b: float):
    try:
        result = divide(a, b)

        logger.info(
            f"Divide operation: {a} / {b} = {result}"
        )

        return {
            "operation": "divide",
            "result": result,
        }

    except ValueError:
        logger.error("Division by zero attempted")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot divide by zero.",
        )


# Older Module 12 registration routes
@app.post(
    "/users/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
@app.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_username = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists.",
        )

    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists.",
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists.",
        )

    logger.info(
        f"New user created: {new_user.username}"
    )

    return new_user


# Older Module 12 login route
@app.post("/users/login")
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.username == login_data.username)
        .first()
    )

    if not user or not verify_password(
        login_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    logger.info(
        f"User logged in: {user.username}"
    )

    return {
        "message": "Login successful.",
        "user_id": user.id,
        "username": user.username,
    }


# Module 13 JWT registration route
@app.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_with_token(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(
            (User.username == user_data.username)
            | (User.email == user_data.email)
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists.",
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists.",
        )

    access_token = create_access_token(
        data={
            "sub": str(new_user.id),
            "username": new_user.username,
            "email": new_user.email,
        }
    )

    logger.info(
        f"New user registered with JWT: "
        f"{new_user.username}"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Registration successful.",
    }


# Module 13 JWT login route
@app.post(
    "/login",
    response_model=TokenResponse,
)
def login_with_token(
    login_data: UserEmailLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if not user or not verify_password(
        login_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
        }
    )

    logger.info(
        f"User logged in with JWT: {user.username}"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful.",
    }


# Add calculation
@app.post(
    "/calculations",
    response_model=CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_calculation(
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = CalculationFactory.calculate(
            calculation_data.a,
            calculation_data.b,
            calculation_data.type,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    new_calculation = Calculation(
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value,
        result=result,
        user_id=current_user.id,
    )

    db.add(new_calculation)
    db.commit()
    db.refresh(new_calculation)

    logger.info(
        f"Calculation created by user "
        f"{current_user.id}: "
        f"{new_calculation.type} "
        f"{new_calculation.a}, "
        f"{new_calculation.b}"
    )

    return new_calculation


# Browse calculations
@app.get(
    "/calculations",
    response_model=list[CalculationRead],
)
def browse_calculations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calculations = (
        db.query(Calculation)
        .filter(
            Calculation.user_id == current_user.id
        )
        .all()
    )

    return calculations


# Read one calculation
@app.get(
    "/calculations/{calculation_id}",
    response_model=CalculationRead,
)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calculation = (
        db.query(Calculation)
        .filter(
            Calculation.id == calculation_id,
            Calculation.user_id == current_user.id,
        )
        .first()
    )

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found.",
        )

    return calculation


# Edit calculation
@app.put(
    "/calculations/{calculation_id}",
    response_model=CalculationRead,
)
def update_calculation(
    calculation_id: int,
    calculation_data: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calculation = (
        db.query(Calculation)
        .filter(
            Calculation.id == calculation_id,
            Calculation.user_id == current_user.id,
        )
        .first()
    )

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found.",
        )

    try:
        result = CalculationFactory.calculate(
            calculation_data.a,
            calculation_data.b,
            calculation_data.type,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    calculation.a = calculation_data.a
    calculation.b = calculation_data.b
    calculation.type = calculation_data.type.value
    calculation.result = result

    db.commit()
    db.refresh(calculation)

    logger.info(
        f"Calculation {calculation.id} updated "
        f"by user {current_user.id}"
    )

    return calculation


# Delete calculation
@app.delete(
    "/calculations/{calculation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calculation = (
        db.query(Calculation)
        .filter(
            Calculation.id == calculation_id,
            Calculation.user_id == current_user.id,
        )
        .first()
    )

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found.",
        )

    db.delete(calculation)
    db.commit()

    logger.info(
        f"Calculation {calculation_id} deleted "
        f"by user {current_user.id}"
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )