import os
import ffmpeg

def cut_video(path_to_video : str, output_folder : str, cut_list : list[tuple[float, float]]):
    filename_without_extension = os.path.splitext(os.path.basename(path_to_video))[0]
    # Loop through the list and create a subclip for each pair of times
    digits = len(str(len(cut_list)))
    for i, (start, end) in enumerate(cut_list):
        # produce file with name like part_01_<filename>.mp4
        output_file_name = f"part_{str(i).zfill(digits)}_{filename_without_extension}.mp4"
        output_file_path = os.path.join(output_folder, output_file_name)

        ffmpeg.input(path_to_video, ss=f"{start}", t=f"{end - start}").output(output_file_path).run()