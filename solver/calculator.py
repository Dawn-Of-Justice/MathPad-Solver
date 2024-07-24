from sympy import symbols, Eq, solve, simplify, sympify


def solve_equation(equation):
    if "=" not in equation:
        raise ValueError("Equation must contain '=' sign.")

    # Replace ^ with ** for power calculations
    equation = equation.replace("^", "**").replace(" ", "")

    left_side, right_side = equation.split("=")

    try:
        if not right_side:
            expr = sympify(left_side)
            return expr.evalf()

        left_side_simplified = sympify(left_side)
        right_side_simplified = sympify(right_side)

        # Determine all symbols in the equation
        all_symbols = (
            left_side_simplified.free_symbols | right_side_simplified.free_symbols
        )
        if not all_symbols:
            raise ValueError("No variables found in the equation.")

        eq = Eq(left_side_simplified, right_side_simplified)

        # Solve for all symbols found
        solutions = solve(eq, all_symbols)
        return solutions
    except Exception as e:
        raise ValueError(f"Error evaluating the equation: {e}")
