import tkinter as tk
from tkinter import messagebox
from gui.drawing_pad import DrawingPad
from solver.calculator import solve_equation


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MathPad Solver")

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=3)  # Larger weight for drawing pad
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)  # New row for the clear button
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Drawing pad section
        self.drawing_pad = DrawingPad(self.root, self.evaluate)
        self.drawing_pad.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Converted text heading
        self.converted_text_heading = tk.Label(self.root, text="Converted Equation")
        self.converted_text_heading.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=5
        )

        # Evaluated expression heading
        self.evaluated_expression_heading = tk.Label(self.root, text="Evaluated Answer")
        self.evaluated_expression_heading.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=5
        )

        # Converted text section
        self.converted_text = tk.Text(self.root, height=5, state=tk.DISABLED)
        self.converted_text.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Evaluated expression section
        self.evaluated_expression = tk.Text(self.root, height=5, state=tk.DISABLED)
        self.evaluated_expression.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        # Clear button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        self.clear_button.grid(row=3, column=0, columnspan=2, pady=10)

    def run(self):
        self.root.mainloop()

    def evaluate(self, event=None):
        equation = self.drawing_pad.get_equation()
        if equation:
            try:
                self.display_converted_text(equation)
                answer = solve_equation(equation)
                if answer:
                    self.display_answer(answer)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def display_converted_text(self, text_equations):
        self.converted_text.config(state=tk.NORMAL)
        self.converted_text.delete(1.0, tk.END)  # Clear existing text

        for equation in text_equations:
            self.converted_text.insert(
                tk.END, equation + "\n"
            )  # Insert each equation followed by a newline

        self.converted_text.config(state=tk.DISABLED)

    def display_answer(self, answer):
        self.evaluated_expression.config(state=tk.NORMAL)
        self.evaluated_expression.delete(1.0, tk.END)  # Clear existing text
        self.evaluated_expression.insert(tk.END, answer)  # Insert new text
        self.evaluated_expression.config(state=tk.DISABLED)

    def clear(self):
        # Clear the drawing pad (Assuming DrawingPad has a clear method)
        self.drawing_pad.clear()

        # Clear the converted text
        self.converted_text.config(state=tk.NORMAL)
        self.converted_text.delete(1.0, tk.END)
        self.converted_text.config(state=tk.DISABLED)

        # Clear the evaluated expression
        self.evaluated_expression.config(state=tk.NORMAL)
        self.evaluated_expression.delete(1.0, tk.END)
        self.evaluated_expression.config(state=tk.DISABLED)
