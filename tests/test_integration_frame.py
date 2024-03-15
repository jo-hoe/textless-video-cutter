from os import path
import unittest

import cv2

from src.frame import Frame 
from src.tesseract_init import Tesseract_Init

class TestIntegrationFrame(unittest.TestCase):

    TEST_FILE_PATH = path.dirname(path.abspath(__file__))
    RESOURCE_PATH = path.join(TEST_FILE_PATH, "resources")    

    @classmethod
    def setUpClass(cls):
        Tesseract_Init.initialize_tesseract()

    def test_is_too_dark_not(self):
        image_path = path.join(self.RESOURCE_PATH, "corgi.jpg")
        image = cv2.imread(image_path)

        frame = Frame(image, 0)

        self.assertFalse(frame.is_too_dark)

    def test_is_too_dark(self):
        image_path = path.join(self.RESOURCE_PATH, "corgi-dark.jpg")
        image = cv2.imread(image_path)

        frame = Frame(image, 0)

        self.assertTrue(frame.is_too_dark)

