from app.models import Calculation, User
from app.schemas import CalculationType
from app.security import hash_password
from app.services.calculation_factory import CalculationFactory
from tests.conftest import TestingSessionLocal


def test_store_calculation_in_database():
    result = CalculationFactory.calculate(
        10,
        5,
        CalculationType.ADD,
    )

    with TestingSessionLocal() as db:
        user = User(
            username="modeltest",
            email="modeltest@example.com",
            password_hash=hash_password("password123"),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        calculation = Calculation(
            a=10,
            b=5,
            type=CalculationType.ADD.value,
            result=result,
            user_id=user.id,
        )

        db.add(calculation)
        db.commit()
        db.refresh(calculation)

        saved_calculation = (
            db.query(Calculation)
            .filter(Calculation.id == calculation.id)
            .first()
        )

        assert saved_calculation is not None
        assert saved_calculation.a == 10
        assert saved_calculation.b == 5
        assert saved_calculation.type == "Add"
        assert saved_calculation.result == 15
        assert saved_calculation.user_id == user.id