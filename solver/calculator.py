from sympy import symbols, Eq, solve, simplify, sympify


def solve_equation(equation):
    if "=" not in equation:
        raise ValueError("Equation must contain '=' sign.")

    equation = equation.replace(" ", "")

    left_side, right_side = equation.split("=")

    try:
        if not right_side:
            expr = sympify(left_side)
            return expr.evalf()

        left_side_simplified = sympify(left_side)
        right_side_simplified = sympify(right_side)

        x = symbols("x")
        eq = Eq(left_side_simplified, right_side_simplified)

        solutions = solve(eq, x)
        return solutions
    except Exception as e:
        raise ValueError(f"Error evaluating the equation: {e}")
