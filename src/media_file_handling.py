import mimetypes
import os


def is_video(path_to_image: str) -> bool:
    return _is_expected_media_type(path_to_image, "video")


def _is_expected_media_type(path_to_image: str, expected_media_type: str):
    if not os.path.isfile(path_to_image):
        raise ValueError(f"File {path_to_image} does not exist")

    mime_type = _get_mime_type(path_to_image)
    return mime_type and mime_type.startswith(expected_media_type)


def _get_mime_type(path_to_image: str) -> str:
    mime_type, _ = mimetypes.guess_type(path_to_image)
    return mime_type


def get_all_filepaths_in_directory(path_to_directory: str) -> list[str]:
    files_and_dirs = os.listdir(path_to_directory)
    paths = list(map(lambda file_name: os.path.join(
        path_to_directory, file_name), files_and_dirs))
    return [f for f in paths if os.path.isfile(f)]
