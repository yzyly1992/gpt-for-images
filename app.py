import gradio as gr
from PIL import Image
import requests
import os
import time
import datetime
from utils import generate_images, process_images, process_video_frames, get_unique_output_path
from image_upscale import upscale_pipeline
from image_generator import image_gen_pipeline

def generate_and_display(prompt=None, size_option=None, image_urls=[]):
    print(prompt)
    print(image_urls)
    return image_gen_pipeline(prompt, image_urls, size_option)
    # return generate_images(prompt, size_option, image_urls)

def upscale_and_download(url, size_option):
    # progress(0, desc="Starting...")
    # progress(0.50, desc="Upscaling...")
    upscaled_img = upscale_pipeline(url, size_option)
    upscaled_image_path = os.path.join("upscale", "upscaled_image_x2.png")
    upscaled_img.save(upscaled_image_path)
    # progress(0.100, desc="Complete")
    return upscaled_image_path

def on_select(evt: gr.SelectData):
    selected_url = evt.value['image']['url']
    return selected_url, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)

def process_and_generate(images, prompt, size_option):
    processed_image_urls = process_images(images)
    return generate_and_display(prompt, size_option, processed_image_urls)

def process_video_and_generate(video, prompt, size_option):
    video_name = os.path.splitext(os.path.basename(video))[0]
    unique_output_path = get_unique_output_path(video_name)
    frame_urls = process_video_frames(video, unique_output_path)
    return generate_and_display(prompt, size_option, frame_urls)

def text_to_image_tab():
    with gr.Row():
        prompt = gr.Textbox(label="Enter your text prompt", placeholder="Type here...")
        size_option = gr.Radio(choices=["65cm x 150cm", "50cm x 60cm"], label="Select Size Option", type="index")
        generate_button = gr.Button("Generate Images")

    with gr.Row():
        image_display = gr.Gallery(label="Generated Images", show_download_button=False)

    selected_image = gr.Textbox(visible=False)
    upscale_button = gr.Button("Upscale & Download Selected Image", visible=False)
    download_file = gr.File(label="Download your upscaled image", visible=False)

    upscale_button.click(fn=upscale_and_download, inputs=[selected_image, size_option], outputs=download_file)
    image_display.select(fn=on_select, inputs=None, outputs=[selected_image, upscale_button, download_file])
    generate_button.click(fn=lambda prompt, size_option: generate_and_display(prompt, size_option), inputs=[prompt, size_option], outputs=image_display)

def image_to_image_tab():
    with gr.Row():
        input_images = gr.File(label="Upload your images", file_count="multiple")
        prompt = gr.Textbox(label="Enter your text prompt", placeholder="Type here...")
        size_option = gr.Radio(choices=["65cm x 150cm", "50cm x 60cm"], label="Select Size Option", type="index")
        process_button = gr.Button("Process Images")

    with gr.Row():
        processed_images = gr.Gallery(label="Processed Images", show_download_button=False)

    selected_image = gr.Textbox(visible=False)
    upscale_button = gr.Button("Upscale & Download Selected Image", visible=False)
    download_file = gr.File(label="Download your upscaled image", visible=False)

    process_button.click(fn=process_and_generate, inputs=[input_images, prompt, size_option], outputs=processed_images)
    processed_images.select(fn=on_select, inputs=None, outputs=[selected_image, upscale_button, download_file])
    upscale_button.click(fn=upscale_and_download, inputs=[selected_image, size_option], outputs=download_file)

def video_tab():
    with gr.Row():
        video_input = gr.Video(label="Upload your video")
        prompt = gr.Textbox(label="Enter your text prompt", placeholder="Type here...")
        size_option = gr.Radio(choices=["65cm x 150cm", "50cm x 60cm"], label="Select Size Option", type="index")
        process_button = gr.Button("Process Video")

    with gr.Row():
        processed_images = gr.Gallery(label="Processed Images", show_download_button=False)

    selected_image = gr.Textbox(visible=False)
    upscale_button = gr.Button("Upscale & Download Selected Image", visible=False)
    download_file = gr.File(label="Download your upscaled image", visible=False)

    process_button.click(fn=process_video_and_generate, inputs=[video_input, prompt, size_option], outputs=processed_images)
    processed_images.select(fn=on_select, inputs=None, outputs=[selected_image, upscale_button, download_file])
    upscale_button.click(fn=upscale_and_download, inputs=[selected_image, size_option], outputs=download_file)

# Define CSS for custom title and background
css = """
body {
    font-family: Arial, sans-serif;
}
h1 {
    text-align: center;
    color: black;
}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("""
    <style>
    body {
        background: linear-gradient(to right, #1f4037, #99f2c8);
        font-family: Arial, sans-serif;
        color: white;
    }
    h1 {
        text-align: center;
        color: black;
    }
    </style>
    <h1>AI Art Generator</h1>
    """)
    with gr.Tabs():
        with gr.TabItem("Text to Image"):
            text_to_image_tab()

        with gr.TabItem("Image to Image"):
            image_to_image_tab()

        with gr.TabItem("Video"):
            video_tab()

demo.launch()
