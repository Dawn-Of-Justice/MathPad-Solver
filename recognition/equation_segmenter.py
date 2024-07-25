import cv2
import numpy as np
from matplotlib import pyplot as plt


class HandwrittenEquationSegmenter:
    def __init__(self, input_shape=(36, 36), y_threshold=40):
        self.input_shape = input_shape
        self.y_threshold = y_threshold
        self.index_to_label = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "add",
            "mul",
            "sub",
            "x",
            "y",
            "z",
        ]

    def preprocess_image(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
        return binary_image

    def detect_connected_components(self, binary_image):
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            binary_image, connectivity=8
        )
        return num_labels, labels, stats, centroids

    def group_components(self, stats):
        bounding_boxes = [
            stats[i][:4] for i in range(1, len(stats))
        ]  # Exclude the background
        bounding_boxes.sort(key=lambda x: x[1])  # Sort by y-coordinate

        equations = []
        current_equation = []

        for i, box in enumerate(bounding_boxes):
            if i == 0:
                current_equation.append(box)
                continue
            if abs(box[1] - bounding_boxes[i - 1][1]) > self.y_threshold:
                equations.append(current_equation)
                current_equation = [box]
            else:
                current_equation.append(box)
        equations.append(current_equation)
        return equations

    def segment_characters(self, binary_image, bounding_boxes, pad_size=30):
        characters = []
        for box in bounding_boxes:
            x, y, w, h = box
            char_image = binary_image[y : y + h, x : x + w]

            # Convert to 3-channel RGB (required for padding function)
            char_image_rgb = cv2.cvtColor(char_image, cv2.COLOR_GRAY2RGB)

            # Pad the image
            char_image_padded = cv2.copyMakeBorder(
                char_image_rgb,
                pad_size,
                pad_size,
                pad_size,
                pad_size,
                cv2.BORDER_CONSTANT,
                value=[0, 0, 0],
            )

            # Resize to input shape
            char_image_resized = cv2.resize(char_image_padded, self.input_shape)

            # Convert back to grayscale
            char_image_gray = cv2.cvtColor(char_image_resized, cv2.COLOR_RGB2GRAY)

            char_image_gray = 255 - char_image_gray  # Invert the image

            # Add channel dimension
            char_image_gray = np.expand_dims(char_image_gray, axis=-1)

            characters.append(char_image_gray)
        return characters

    def display_characters(self, char_images):
        plt.figure(figsize=(12, 6))
        for i, char_image in enumerate(char_images):
            plt.subplot(1, len(char_images), i + 1)
            plt.imshow(char_image.squeeze(), cmap="gray")
            plt.axis("off")
        plt.show()

    def draw_equations(self, image, bounding_boxes, recognized_characters):
        color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        for i, (box, char) in enumerate(zip(bounding_boxes, recognized_characters)):
            x, y, w, h = box
            cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                color_image,
                char,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2,
            )
        return color_image

    def recognize_characters(self, char_images, model):
        recognized_sequence = []
        for char_image in char_images:
            char_image = np.expand_dims(char_image, axis=0)  # Add batch dimension
            predictions = model.predict(char_image, verbose=0)
            predicted_class = np.argmax(predictions, axis=1)
            recognized_char = self.index_to_label[predicted_class[0]]
            recognized_sequence.append(recognized_char)

        # Post-process to correct specific misclassifications
        corrected_sequence = []
        i = 0
        while i < len(recognized_sequence):
            print(recognized_sequence)
            if recognized_sequence[i] == "sub":
                if (
                    i + 2 < len(recognized_sequence)
                    and recognized_sequence[i + 1] == "0"
                    and recognized_sequence[i + 2] == "0"
                ):
                    corrected_sequence.append("div")
                    i += 3  # Skip the next '0' and '0' as they are combined with 'div'
                elif (
                    i + 1 < len(recognized_sequence)
                    and recognized_sequence[i + 1] == "sub"
                ):
                    corrected_sequence.append("eq")
                    i += 2  # Skip the next 'div' as it's combined with the current one
                else:
                    corrected_sequence.append("sub")
                    i += 1
            else:
                corrected_sequence.append(recognized_sequence[i])
                i += 1

        return corrected_sequence

    def process_image(self, image_path, model, debug=False, pad_size=5):
        binary_image = self.preprocess_image(image_path)
        original_image = cv2.imread(
            image_path, cv2.IMREAD_GRAYSCALE
        )  # Load original image for drawing
        num_labels, labels, stats, centroids = self.detect_connected_components(
            binary_image
        )
        equations = self.group_components(stats)

        all_recognized_characters = []
        text_equations = []

        symbol_mapping = {"add": "+", "sub": "-", "mul": "*", "div": "/", "eq": "="}

        for equation in equations:
            bounding_boxes = [tuple(stats[i + 1][:4]) for i in range(len(stats) - 1)]

            filtered_boxes = []
            for box in bounding_boxes:
                x, y, w, h = box
                for eq_box in equation:
                    eq_x, eq_y, eq_w, eq_h = eq_box
                    if (x, y, w, h) == (eq_x, eq_y, eq_w, eq_h):
                        filtered_boxes.append(box)
                        break

            filtered_boxes.sort(key=lambda b: b[0])  # Sort by x-coordinate

            characters = self.segment_characters(binary_image, filtered_boxes, pad_size)
            if debug:
                self.display_characters(characters)

            recognized_characters = self.recognize_characters(characters, model)
            print(recognized_characters)
            all_recognized_characters.append(recognized_characters)

            # Convert recognized characters to text
            text_equation = "".join(
                [symbol_mapping.get(char, char) for char in recognized_characters]
            )
            # Handle duplicate '=' detection
            if "==" in text_equation:
                text_equation = text_equation.replace("==", "=")

            text_equations.append(text_equation)

            if debug:
                image_with_equations = self.draw_equations(
                    original_image, filtered_boxes, recognized_characters
                )
                cv2.imshow("Recognized Equations", image_with_equations)
                cv2.waitKey(0)  # Wait for a key press to close the window
                cv2.destroyAllWindows()  # Close the window

        return text_equations
