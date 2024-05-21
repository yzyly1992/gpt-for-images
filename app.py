import gradio as gr
# from image_generator import generate_images
from image_upscale import upscale_image,resize_to_target_size
import requests
import tempfile
import os
from PIL import Image
os.makedirs("images", exist_ok=True)
os.makedirs("upscale", exist_ok=True)
os.makedirs("samples", exist_ok=True)

def generate_images(prompt, n_images=4):
    print('Generating images...')
    # Returning static URLs for testing purposes
    return [
        'https://cl.imagineapi.dev/assets/71f4b2d8-7d3b-4c83-9ccb-25b67c3ffc55/71f4b2d8-7d3b-4c83-9ccb-25b67c3ffc55.png',
        'https://cl.imagineapi.dev/assets/185ad9c1-74c0-4789-bf9f-914eab39faee/185ad9c1-74c0-4789-bf9f-914eab39faee.png',
        'https://cl.imagineapi.dev/assets/62205ff8-0ec1-4d95-b8d8-2a68a58b4151/62205ff8-0ec1-4d95-b8d8-2a68a58b4151.png',
        'https://cl.imagineapi.dev/assets/489904a3-0820-4f3d-af7d-ab3d1016ca0e/489904a3-0820-4f3d-af7d-ab3d1016ca0e.png'
    ]
def generate_and_display(prompt):
    image_urls = generate_images(prompt)
    return image_urls

def resize_image(image_path, target_size):
    with Image.open(image_path) as img:
        img = img.resize(target_size)
        img.save(image_path)

def upscale_and_download(url,progress=gr.Progress(track_tqdm=True)):
    progress(0, desc="Starting...")
    response = requests.get(url)
   
    file_name = os.path.join("images", url.split("/")[-1])
    with open(file_name, "wb") as file:
        file.write(response.content)
    upscaled_image_path = "samples/upscaled_image.png"
    # Upscale the image
    progress(50, "Resizing image to 1024x1024...")
    resize_image(file_name, (1024, 1024))
    # upscale_image(file_name, upscaled_image_path)
    # # Resize the upscaled image to the target size
    # resize_to_target_size(upscaled_image_path, (2048, 2048))
    # return upscaled_image_path
    # return download_image(upscaled_url)

def on_select(evt: gr.SelectData):
    # Extract the actual URL from the metadata
    selected_url = evt.value['image']['url']
    return selected_url, gr.update(visible=True), gr.update(visible=True)

with gr.Blocks() as demo:
    with gr.Row():
        prompt = gr.Textbox(label="Enter your prompt", placeholder="Type here...")
        generate_button = gr.Button("Generate Images")

    with gr.Row():
        image_display = gr.Gallery(label="Generated Images",show_download_button=False)

    selected_image = gr.Textbox(visible=False)
    download_output = gr.File(label="Downloaded Image", visible=False)
    upscale_output = gr.File(label="Upscaled Image", visible=False)
    progress_text = gr.Textbox(label="Progress", visible=False)
    
    # download_button = gr.Button("Download Selected Image", visible=False)
    # download_button.click(fn=download_image, inputs=selected_image, outputs=download_output)
    
    upscale_button = gr.Button("Upscale & Download Selected Image", visible=False)
    upscale_button.click(fn=upscale_and_download, inputs=selected_image, outputs=upscale_output)

    image_display.select(fn=on_select, inputs=None, outputs=[selected_image, upscale_button])
    
    generate_button.click(fn=generate_and_display, inputs=prompt, outputs=image_display)

   

    with gr.Row():
        upscale_button
        progress_text

demo.launch()
