import numpy as np
from typing import Tuple
from Model import process_frame


def process_click(frame: np.array, curser_position: Tuple[int, int], color_to_paint: Tuple[np.uint8, np.uint8, np.uint8]) \
        -> np.ndarray:
    labels = process_frame(frame)
    width, height, channels = frame.shape
    blur = np.zeros_like(frame)
    mask = labels == labels[curser_position]
    mask = np.repeat(mask[:, :, np.newaxis], channels, axis=2)

    # Apply the Gaussian blur for background with the kernel size specified in constants above

    if color_to_paint is not None:
        blur[:, :] = color_to_paint
        frame[mask] = 0.7 * frame[mask] + 0.3 * blur[mask]
    return frame


