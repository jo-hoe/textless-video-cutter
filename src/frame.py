import cv2
import numpy as np
import pytesseract


class Frame():

    DARKNESS_THRESHOLD = 10

    def __init__(self, frame, timestamp):
        self._timestamp = timestamp

        self._is_frame_too_dark = self._is_too_dark(frame)
        self._is_frame_has_text = self._has_text(frame)

        self._is_valid = not self._is_frame_too_dark and not self._is_frame_has_text

    def _is_too_dark(self, frame):
        '''
        # Define a function to check if a frame is too dark
        '''
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate the mean pixel value
        mean = np.mean(gray)
        # If the mean is close to zero, the frame is black
        return mean < self.DARKNESS_THRESHOLD


    def _has_text(self, frame):
        text = pytesseract.image_to_string(frame)
        # If the text is not empty, the frame contains text
        if text == "":
            return False
        else:
            return True

    @property
    def is_too_dark(self):
        return self._is_frame_too_dark

    @property
    def has_text(self):
        return self._is_frame_has_text
    
    @property
    def get_timestamp(self):
        return self._timestamp
    
    @property
    def is_valid(self):
        return self._is_valid

    @property
    def __str__(self):
        return f"dark:{self._is_too_dark}; has text:{self._is_frame_has_text}"