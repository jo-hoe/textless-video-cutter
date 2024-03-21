import os
import cv2
import uuid
import threading

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.frame import Frame

from src.media_file_handling import is_video


def analyse_frame_for_valid_sections(timestamp: float, frame) -> Frame:
    return Frame(frame, timestamp)


def analyse_video_for_valid_sections(video_path: str, sample_rate_in_Hz: int = 2) -> list[Frame]:
    if not is_video(video_path):
        raise ValueError(f"File {video_path} is not an image file")

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Calculate how many frames to skip
    fps = video.get(cv2.CAP_PROP_FPS)
    step_size = int(fps / sample_rate_in_Hz)

    # create loading bar
    total_frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video_name = os.path.basename(video_path)
    loading_bar = tqdm(total=(total_frame_count - step_size),
                       desc=f"analyzing video '{video_name}'")

    frame_count = 0
    results = []
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = []
        while video.isOpened():
            # Read a frame from the video
            is_valid_frame, frame = video.read()
            # If the frame is valid, process it
            if not is_valid_frame:
                break

            # Calculate the timestamp of the frame
            timestamp = frame_count / fps
            # schedule the frame processing function
            future = executor.submit(
                analyse_frame_for_valid_sections, timestamp, frame)
            futures.append(future)

            # Increment the frame counter
            frame_count += step_size
            # Skip the next frame
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_count + step_size)

            loading_bar.update(step_size)

        # get the results as they are ready
        for future in as_completed(futures):
            results.append(future.result())

    loading_bar.close()
    video.release()

    sorted_result = sorted(results, key=lambda x: x.get_timestamp)
    return sorted_result


def get_valid_intervals(frames: list[Frame], noise_threshold=1):
    if noise_threshold < 1:
        ValueError(f"noise_threshold cannot be below 1")

    valid_intervals = []

    start = None
    end = None

    invalid_count = 0
    for frame in frames:
        if frame.is_valid:
            if start is None:
                start = frame.get_timestamp
            end = frame.get_timestamp

            invalid_count = 0
        else:
            invalid_count += 1
            # if the invalid count exceeds the noise threshold
            if invalid_count >= noise_threshold:
                # if the start and end are not None, append the interval to the list
                if start is not None and end is not None:
                    valid_intervals.append((start, end))

                start = None
                end = None
    # after the loop, if the start and end are not None, append the interval to the list
    if start is not None and end is not None:
        valid_intervals.append((start, end))

    return valid_intervals


def filter_intervals(intervals: list[tuple[float, float]], min_length_in_seconds=2):
    result = []
    for start, end in intervals:
        if end - start > min_length_in_seconds:
            result.append((start, end))

    return result


def showImage(img):
    """
    Only used for debugging purposes
    Show an image in a new window
    Args:
        img: The image to show
    """

    def show(img):
        cv2.imshow(str(uuid.uuid4()), img)
        cv2.waitKey()

    threading.Thread(target=show, args=[img]).start()
