# gpt-for-images

The system accepts inputs in the form of images, videos, and text prompts. Through a web interface provided by Gradio, users can upload images or videos or text prompts. The system utilizes the Midjourney API for AI-driven image generation. Additionally, it incorporates an AI upscaling API to adjust image resolutions for large print dimensions. Post-processing techniques such as format conversion and applying filters are then applied to enhance the final output. The result is an image ready for printing and downloading.

### Development Tools

Language: Python   
Library: requests, pillow   
GUI: gradio   
API: imagineapi.dev (Midjourney API), stability.ai (Upscaling API), ImgBB (Image Hosting API)   
