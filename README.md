# MathPad Solver

## Overview

This project aims to create a Python application that can recognize and solve handwritten mathematical equations in real-time. Users can write equations using a graphical interface, and the program will recognize the handwritten text, parse the equation, solve it, and display the result.

## Features

- **Handwriting Recognition**: Uses OCR to recognize handwritten numbers and basic mathematical operators.
- **Equation Parsing**: Extracts and simplifies mathematical expressions from recognized text.
- **Real-Time Calculation**: Solves the equation and displays the result immediately.
- **User-Friendly Interface**: Simple writing pad interface for easy user input.


### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Dawn-Of-Justice/MathPad-Solver.git
   cd MathPad-Solver
   ```

2. **Install Tesseract**

   Ensure that you have installed Tesseract on your system and the path to it is set in the config.py.

   On Ubuntu, you can install Tesseract using:

   ```bash
   sudo apt-get install tesseract-ocr
   ```

   On macOS, you can use Homebrew:

   ```bash
   brew install tesseract
   ```

   On Windows, download the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and follow the installation instructions.

3. **Install Python Dependencies**

   Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Tesseract Path**

   Ensure the path to the Tesseract executable is set in config.py. For example:

   ```python
   TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
   # or
   TESSERACT_CMD = '/usr/local/bin/tesseract'  # macOS/Linux
   ```


4. **Running**

   Run the main.py file to get your program up and running:

   ```bash
   python main.py
   ```

### Usage

1. Write your equation on the graphical writing pad interface.
2. The application will recognize the handwritten text and display the recognized equation.
3. The application will parse the equation, solve it, and display the result in real-time.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contact

For any questions or suggestions, please open an issue on the GitHub repository.
