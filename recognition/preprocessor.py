import math
from typing import Tuple, Union
import cv2
import numpy as np
from deskew import determine_skew


def rotate(
    image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(
        np.cos(angle_radian) * old_width
    )
    height = abs(np.sin(angle_radian) * old_width) + abs(
        np.cos(angle_radian) * old_height
    )

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(
        image, rot_mat, (int(round(height)), int(round(width))), borderValue=background
    )


def preprocess_image(image_path):

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image at path '{image_path}' could not be read.")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    angle = determine_skew(img_gray)
    rotated = rotate(img_gray, angle, (0, 0, 0))
    _, img_bin = cv2.threshold(rotated, 128, 255, cv2.THRESH_BINARY_INV)
    img_bin = cv2.medianBlur(img_bin, 3)
    preprocessed_image_path = "captured_image.png"

    return preprocessed_image_path
