import unittest
from os import path

import cv2
from src import video_analysis
from src.frame import Frame
from src.tesseract_init import Tesseract_Init

class TestIntegrationVideoAnalyse(unittest.TestCase):
    
    TEST_FILE_PATH = path.dirname(path.abspath(__file__))
    RESOURCE_PATH = path.join(TEST_FILE_PATH, "resources")    

    @classmethod
    def setUpClass(cls):
        Tesseract_Init.initialize_tesseract()

    def test_video_processing_sampling_rate(self):
        sample_rate = 3
        video_path = path.join(self.RESOURCE_PATH, "video_no_text.mp4")
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

        result = video_analysis.analyse_video_for_valid_sections(video_path,sample_rate)

        actual_length = len(result)
        expected_length = int((total_frame_count / (fps / sample_rate)))
        deviation = abs(actual_length - expected_length)
        
        self.assertLessEqual(deviation, 1, f"Unexpected number of results. Found {actual_length} while expected {expected_length}")

    def test_video_processing_with_text(self):
        video_path = path.join(self.RESOURCE_PATH, "video_with_text.mp4")

        result = video_analysis.analyse_video_for_valid_sections(video_path)

        number_of_frames_with_text = 0
        number_of_frames_without_text = 0
        for frames in result:
            if frames.has_text:
                number_of_frames_with_text += 1
            else:
                number_of_frames_without_text += 1

        self.assertGreater(number_of_frames_without_text, 0, "found no images without text")
        self.assertGreater(number_of_frames_with_text, 0, "found no images with text")
