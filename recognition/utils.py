import re


def clean_equation(equation_text):

    cleaned_equation = re.sub(r"\s+", "", equation_text)
    cleaned_equation = cleaned_equation.replace("\n", "").replace("\r", "")

    return cleaned_equation
