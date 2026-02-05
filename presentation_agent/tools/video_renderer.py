from moviepy import ImageClip, concatenate_videoclips

def make_video(images, durations):
    """
    Creates a video from a list of image paths and their display durations.
    
    Args:
        images: list of str — paths to image files
        durations: list of float/int — duration in seconds for each image
    
    Returns:
        str — path to the created video file
    """
    clips = []
    
    for img_path, duration in zip(images, durations):
        clip = ImageClip(img_path).with_duration(duration)
        clips.append(clip)
    
    # method="compose" is still supported, but most common use-case now is default
    video = concatenate_videoclips(clips, method="compose")
    
    output_path = "workspace/output/presentation.mp4"
    
    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",          # usually safe default
        preset="medium",            # balance between speed & size
        threads=None,               # auto = good choice on most machines
        logger=None                 # set to 'bar' if you want progress bar
    )
    
    return output_path
