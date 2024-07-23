import pytesseract
from PIL import Image
from config import TESSERACT_PATH
from .preprocessor import preprocess_image
from .utils import clean_equation

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def ocr_recog(image_path, debug=False):
    preprocessed_image_path = preprocess_image(image_path)
    img = Image.open(preprocessed_image_path)
    

    text = pytesseract.image_to_string(img, config="--oem 1 --psm 6")

    if debug == True:
        print("Detected Text:")
        print(text)

    cleaned_text = clean_equation(text)
    return cleaned_text
