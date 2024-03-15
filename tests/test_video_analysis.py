import unittest

from src import video_analysis
from src.frame import Frame



class TestVideoAnalyse(unittest.TestCase):

    def test_filter_intervals(self):
        cut_list = [(0.0, 2.4), (3.36, 4.32)]

        result = video_analysis.filter_intervals(cut_list, 1)

        self.assertEqual(result, [(0.0, 2.4)])

    def test_get_valid_intervals(self):
        input_basic = [(0.0, True), (0.48, True), (0.96, True), (1.44, True),
                  (1.92, True), (2.4, True), (2.88, False), (3.36, True), (3.84, True), (4.32, True)]

        input = []
        for tuple in input_basic:
            frame = MockFrame(tuple[0], tuple[1])
            input.append(frame)

        result = video_analysis.get_valid_intervals(input, 1)

        self.assertEqual(result[0], (0.0, 2.4))
        self.assertEqual(result[1], (3.36, 4.32))

    def test_get_valid_intervals_noise_threshold(self):
        input_basic = [(0.0, True), (0.48, True), (0.96, False), (1.44, True),
                  (1.92, True), (2.4, True), (2.88, False), (3.36, False), (3.84, True), (4.32, True)]

        input = []
        for tuple in input_basic:
            frame = MockFrame(tuple[0], tuple[1])
            input.append(frame)

        result = video_analysis.get_valid_intervals(input, 2)

        self.assertEqual(result[0], (0.0, 2.4))
        self.assertEqual(result[1], (3.84, 4.32))

    def test_get_valid_intervals_with_invalid_in_start_and_end(self):
        input_basic = [(0.0, False), (2, True), (3, True), (4, False),
                  (5, True), (6, True), (7, False)]

        input = []
        for tuple in input_basic:
            frame = MockFrame(tuple[0], tuple[1])
            input.append(frame)

        result = video_analysis.get_valid_intervals(input, 1)

        self.assertEqual(result[0], (2, 3))
        self.assertEqual(result[1], (5, 6))



class MockFrame():
    def __init__(self, timestamp, is_valid):
        self._mock_timestamp = timestamp
        self._mock_is_valid = is_valid

    @property
    def is_valid(self):
        return self._mock_is_valid

    @property
    def get_timestamp(self):
        return self._mock_timestamp