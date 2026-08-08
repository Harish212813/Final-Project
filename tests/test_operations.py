import pytest

from app.operations import (
    add,
    divide,
    modulus,
    multiply,
    power,
    subtract,
)


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(4, 3) == 12


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)


def test_power():
    assert power(2, 3) == 8


def test_power_zero_exponent():
    assert power(5, 0) == 1


def test_modulus():
    assert modulus(10, 3) == 1


def test_modulus_by_zero():
    with pytest.raises(ValueError):
        modulus(10, 0)