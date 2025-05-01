import ffmpeg

def create_trip_video(image_folder, audio_path, output_path):
    (
        ffmpeg
        .input(f"{image_folder}/*.jpg", pattern_type='glob', framerate=1)
        .output(output_path, vcodec='libx264', acodec='aac', audio=audio_path)
        .run()
    )
