from functools import cache
import os
import pytesseract

class Tesseract_Init():
    '''
    On Windows we have to provide the path to tesseract.
    This class initializes the path to tesseract in case it is needed.
    '''
    DEFAULT_PATH = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    @cache # <- ensures that method is only called once if same args
    @staticmethod
    def initialize_tesseract(tesseract_path : str = DEFAULT_PATH):
        if os.name == 'nt':
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    @staticmethod
    def get_default_path() -> str:
        if os.name == 'nt':
            return Tesseract_Init.DEFAULT_PATH
        
        return None