## extract key frames from video using moviepy

import os
import sys
from moviepy.editor import VideoFileClip 

def video_to_image(video_path, output_path, num_frames=5):
    video = VideoFileClip(video_path)
    duration = int(video.duration)
    print(f'duration: {duration}')
    fps = duration // (num_frames + 1)
    for i in range(fps//2, duration, fps):
        video.save_frame(os.path.join(output_path, f'{i}.jpg'), t=i)

if __name__ == '__main__':
    video_path = sys.argv[1]
    output_path = sys.argv[2]
    video_to_image(video_path, output_path)
    # video_path = 'samples/the_last_of_us.mp4'
    # output_path = 'samples/the_last_of_us'
    # video_to_image(video_path, output_path)