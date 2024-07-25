import re
from sympy import symbols, Eq, solve, sympify

def preprocess_equation(equation):
    # Add * between numbers and variables
    equation = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation)
    # Add spaces around operators for proper sympy parsing
    equation = re.sub(r'([\+\-\*/\^=])', r' \1 ', equation)
    return equation

def solve_equation(equations):
    if isinstance(equations, str):
        equations = [equations]

    if not isinstance(equations, list):
        raise ValueError("Input must be a string or a list of strings.")

    solutions = []
    
    for equation in equations:
        try:
            # Preprocess the equation
            equation = preprocess_equation(equation)

            if "=" in equation:
                left_side, right_side = equation.split("=")
            else:
                left_side = equation
                right_side = '0'

            left_side_simplified = sympify(left_side)
            right_side_simplified = sympify(right_side)

            # Determine if it's a simple arithmetic expression
            if not left_side_simplified.free_symbols and not right_side_simplified.free_symbols:
                result = left_side_simplified - right_side_simplified
                solutions.append(result.evalf())
                continue

            # Determine all symbols in the equation
            all_symbols = (
                left_side_simplified.free_symbols | right_side_simplified.free_symbols
            )
            if not all_symbols:
                raise ValueError("No variables found in the equation.")

            eq = Eq(left_side_simplified, right_side_simplified)

            # Solve for all symbols found
            solution = solve(eq, all_symbols)
            solutions.append(solution)
        except Exception as e:
            pass

    # If more than one equation is provided, solve the system of equations
    if len(solutions) > 1:
        symbols_list = []
        eqs = []

        for equation in equations:
            if "=" in equation:
                left_side, right_side = equation.split("=")
            else:
                left_side = equation
                right_side = '0'
            left_side = preprocess_equation(left_side)
            right_side = preprocess_equation(right_side)
            try:
                eq = Eq(sympify(left_side), sympify(right_side))
            except Exception as e:
                continue
            eqs.append(eq)
            symbols_list.extend(list(eq.free_symbols))

        symbols_set = set(symbols_list)
        try:
            system_solution = solve(eqs, symbols_set)
            return system_solution
        except Exception as e:
            pass

    return solutions[0] if len(solutions) == 1 else solutions