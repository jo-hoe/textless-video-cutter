import os
import shutil
import uuid
import ffmpeg
import unittest
import tempfile

from src import video_processing
from src.media_file_handling import get_all_filepaths_in_directory
from src.tesseract_init import Tesseract_Init

class TestIntegrationProcessing(unittest.TestCase):
    
    TEST_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    RESOURCE_PATH = os.path.join(TEST_FILE_PATH, "resources")    

    def setUp(self):
        self.working_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        os.makedirs(self.working_dir)
        self.artifact_folder = self.working_dir

    def tearDown(self):
        if os.path.exists(self.artifact_folder):
            shutil.rmtree(self.artifact_folder) 

    @classmethod
    def setUpClass(cls):
        Tesseract_Init.initialize_tesseract()

    def test_video_processing_sampling_rate(self):
        cut_list = [(0.0, 2.4), (3.36, 4.32)]
        file_path = os.path.join(self.RESOURCE_PATH, "video_with_text.mp4")

        video_processing.cut_video(file_path, self.working_dir, cut_list)

        file_paths = get_all_filepaths_in_directory(self.working_dir)

        self.assertEqual(len(file_paths), len(cut_list), "unexpected number of files")
        sorted_all_output_files = sorted(file_paths, key=len)
        for i in range(len(sorted_all_output_files)):
            info = ffmpeg.probe(sorted_all_output_files[i])
            # Get the duration of the video file in seconds
            duration = float(info["format"]["duration"])

            self.assertAlmostEqual(cut_list[i][1] - cut_list[i][0], duration, msg="unexpected video duration")