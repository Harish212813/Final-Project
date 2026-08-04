import pytest
from pydantic import ValidationError

from app.schemas import (
    CalculationCreate,
    CalculationRead,
    CalculationType,
)


def test_calculation_create_valid():
    calculation = CalculationCreate(
        a=10,
        b=5,
        type="Add",
    )

    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == CalculationType.ADD


def test_calculation_create_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b=5,
            type="Power",
        )


def test_calculation_create_divide_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b=0,
            type="Divide",
        )


def test_calculation_read_schema():
    calculation = CalculationRead(
        id=1,
        a=8,
        b=2,
        type="Divide",
        result=4,
        user_id=1,
    )

    assert calculation.id == 1
    assert calculation.result == 4
    assert calculation.user_id == 1