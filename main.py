import argparse
import os
from src import video_analysis, video_processing

from src.media_file_handling import get_all_filepaths_in_directory, is_video
from src.tesseract_init import Tesseract_Init

def run(input_directory : str, output_directory : str, sample_rate : int, 
        min_output_length : float, noise_threshold : int, tesseract_ocr_path : str):
    Tesseract_Init.initialize_tesseract(tesseract_ocr_path)

    if not os.path.isdir(input_directory):
        raise ValueError(f"input directory {input_directory} does not exist")
    
    if output_directory == None:
        output_directory = input_directory
    else:
        if not os.path.isdir(output_directory):
            raise ValueError(f"output directory {output_directory} does not exist")
        
    filepaths = get_all_filepaths_in_directory(input_directory)
    video_files = [f for f in filepaths if is_video(f)]

    for video_path in video_files:
        all_frames = video_analysis.analyse_video_for_valid_sections(video_path, sample_rate)
        valid_sections = video_analysis.get_valid_intervals(all_frames, noise_threshold)
        filters_sections = video_analysis.filter_intervals(valid_sections, min_output_length)
        video_processing.cut_video(video_path, output_directory, filters_sections)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cut section from video which are not too dark and do not contain text')
    parser.add_argument('--input-directory', dest='input_directory', type=str, required=True,
                        help='Directory that contains videos')
    parser.add_argument('--output-directory', dest='output_directory', type=str, required=False, default=None,
                        help='Directory where the output should be stored')
    parser.add_argument('--sample-rate', dest='sample_rate', type=int, required=False, default=3,
                        help='Sample rate in Hz')
    parser.add_argument('--output-min-length', dest='output_min_length', type=float, required=False, default=2,
                        help='Min length of a output video section in seconds')
    parser.add_argument('--noise-threshold', dest='noise_threshold', type=int, required=False, default=1,
                        help='Min number of frame which are detected as invalid before a cut is executed')
    parser.add_argument('--tesseract-ocr-path', dest='tesseract_ocr_path', type=str, required=False, default=Tesseract_Init.get_default_path(),
                        help='Path to tesseract-ocr. This as only to be provided if your are on windows and the .exe is not installed in the default folder')
    args = parser.parse_args()


    run(args.input_directory, args.output_directory, args.sample_rate, args.output_min_length, args.noise_threshold, args.tesseract_ocr_path)
