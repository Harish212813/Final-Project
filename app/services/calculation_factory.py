from app.schemas import CalculationType


class CalculationFactory:
    @staticmethod
    def calculate(
        a: float,
        b: float,
        calculation_type: CalculationType,
    ) -> float:
        if calculation_type == CalculationType.ADD:
            return a + b

        if calculation_type == CalculationType.SUBTRACT:
            return a - b

        if calculation_type == CalculationType.MULTIPLY:
            return a * b

        if calculation_type == CalculationType.DIVIDE:
            if b == 0:
                raise ValueError("Cannot divide by zero")
            return a / b

        if calculation_type == CalculationType.POWER:
            return a ** b

        if calculation_type == CalculationType.MODULUS:
            if b == 0:
                raise ValueError("Cannot perform modulus by zero")
            return a % b

        raise ValueError("Invalid calculation type")