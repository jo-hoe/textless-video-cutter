# textless-video-cutter

Takes video as input and generates video subsections that do not contain text or a dark image.

## pre-requisites

- [ffmpeg](https://ffmpeg.org/download.html)

## video pre-processing

In case you want to crop the video before you cut it, you can do so by using ffmpeg.

### Command to preview video

```bash
ffplay -i input.mp4 -filter:v "crop=in_w-100:in_h-100:50:50" output.mp4
```

### Command to create a new cropped video

```bash
ffmpeg -i input.mp4 -filter:v "crop=in_w-100:in_h-100:50:50" output.mp4
```
