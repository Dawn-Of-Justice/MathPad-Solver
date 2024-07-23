from .calculator import solve_equation


def parse_and_solve_equation(equation):
    """
    Parses the equation and calls solve_equation only if '=' is present.
    """
    if "=" in equation:
        try:
            result = solve_equation(equation)
            return result
        except Exception as e:
            return f"Error solving equation: {e}"
