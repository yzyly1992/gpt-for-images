# app.py
import gradio as gr
from image_generator import generate_image_from_text, generate_image_from_image, generate_image_from_video

# Define interfaces for text, image, and video input
text_to_image_interface = gr.Interface(
    fn=generate_image_from_text,
    inputs=gr.Textbox(label="Enter Text"),
    outputs=gr.Image(label="Generated Image"),
    title="Text to Image",
    description="Generate an image from a text prompt using the Imagine API."
)

image_to_image_interface = gr.Interface(
    fn=generate_image_from_image,
    inputs=gr.Image(label="Upload Image"),
    outputs=gr.Image(label="Generated Image"),
    title="Image to Image",
    description="Generate a new image from an uploaded image using the Imagine API."
)

video_to_image_interface = gr.Interface(
    fn=generate_image_from_video,
    inputs=gr.Video(label="Upload Video"),
    outputs=gr.Image(label="Generated Image"),
    title="Video to Image",
    description="Generate an image from a video using the Imagine API."
)

# Combine all interfaces into one
iface = gr.TabbedInterface(
    [text_to_image_interface, image_to_image_interface, video_to_image_interface],
    ["Text to Image", "Image to Image", "Video to Image"]
)

if __name__ == "__main__":
    iface.launch()