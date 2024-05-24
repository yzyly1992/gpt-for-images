import os
import datetime
from PIL import Image
from image_to_url import image_to_url
from video_to_image import video_to_image
os.makedirs("images", exist_ok=True)

def generate_images(prompt=None, size_option=None, image_urls=None, n_images=4):
    print('Generating images with size option:', size_option)
    return [
        'https://cl.imagineapi.dev/assets/71f4b2d8-7d3b-4c83-9ccb-25b67c3ffc55/71f4b2d8-7d3b-4c83-9ccb-25b67c3ffc55.png',
        'https://cl.imagineapi.dev/assets/185ad9c1-74c0-4789-bf9f-914eab39faee/185ad9c1-74c0-4789-bf9f-914eab39faee.png',
        'https://cl.imagineapi.dev/assets/62205ff8-0ec1-4d95-b8d8-2a68a58b4151/62205ff8-0ec1-4d95-b8d8-2a68a58b4151.png',
        'https://cl.imagineapi.dev/assets/489904a3-0820-4f3d-af7d-ab3d1016ca0e/489904a3-0820-4f3d-af7d-ab3d1016ca0e.png'
    ]

def process_images(images):
    processed_images = []
    for img_file in images:
        img = Image.open(img_file.name)
        temp_path = os.path.join("images", img_file.name.split('/')[-1])
        img.save(temp_path)
        image_url = image_to_url(temp_path)
        processed_images.append(image_url)
    return processed_images

def process_video_frames(video_path, output_path):
    video_to_image(video_path, output_path)
    frame_urls = []
    for frame_file in os.listdir(output_path):
        frame_path = os.path.join(output_path, frame_file)
        frame_url = image_to_url(frame_path)
        frame_urls.append(frame_url)
    return frame_urls

def get_unique_output_path(video_name, base_dir="video_frames"):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_dir_name = f"{video_name}_{current_time}"
    output_path = os.path.join(base_dir, unique_dir_name)
    os.makedirs(output_path, exist_ok=True)
    return output_path
