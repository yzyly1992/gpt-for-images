## extract key frames from video using moviepy

import os
import argparse
from moviepy.editor import VideoFileClip 

def video_to_image(video_path, output_path, num_frames=5):
    video = VideoFileClip(video_path)
    duration = int(video.duration)
    print(f'duration: {duration}')
    fps = duration // (num_frames + 1)
    for i in range(fps//2, duration, fps):
        video.save_frame(os.path.join(output_path, f'{i}.jpg'), t=i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--num_frames', type=int, default=5)
    args = parser.parse_args()
    video_to_image(args.video_path, args.output_path, args.num_frames)
    # video_path = 'samples/the_last_of_us.mp4'
    # output_path = 'samples/the_last_of_us'
    # video_to_image(video_path, output_path)