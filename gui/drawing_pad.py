import os
import tkinter as tk
from PIL import ImageGrab
from recognition import HandwrittenEquationSegmenter
from tensorflow.keras.models import load_model # type: ignore

class DrawingPad(tk.Frame):
    def __init__(self, parent, evaluate_callback):
        super().__init__(parent)
        self.evaluate_callback = evaluate_callback
        self.canvas = tk.Canvas(self, bg="white", width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.last_x, self.last_y = None, None
        self.equation_text = tk.StringVar()
        self.answer_label = tk.Label(self, text="", font=("Arial", 12))
        self.answer_label.pack()
        self.loaded_model = load_model(r'C:\Users\salos\MathPad-Solver\recognition\custom_model\test_model.h5')
        self.segmenter = HandwrittenEquationSegmenter()

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y

    def on_button_release(self, event):
        self.last_x, self.last_y = None, None
        self.evaluate_callback(event)

    def paint(self, event):
        # Get the current mouse position
        x, y = event.x, event.y

        # Check if there is a previous position to draw a line from
        if self.last_x is not None and self.last_y is not None:
            # Draw a line from the last position to the current position
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                x,
                y,
                width=10,
                fill="black",
                capstyle=tk.ROUND,
                smooth=True,
            )

        # Update the last position
        self.last_x, self.last_y = x, y

    def get_equation(self):
        # Get the image of the drawing
        x = self.winfo_rootx() + self.canvas.winfo_x()
        y = self.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        image = ImageGrab.grab().crop((x, y, x1, y1))
        image_path = os.path.join(os.getcwd(), "captured_image.png")
        image.save(image_path)
        equations = self.segmenter.process_image(image_path, self.loaded_model)
        return equations

    def clear(self):
        self.canvas.delete("all")
        self.answer_label.config(text="")
