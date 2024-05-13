# gpt-for-images

The system accepts inputs in the form of images, videos, and text prompts. Through a web interface provided by Gradio, users can upload images or videos or text prompts. The system utilizes the Midjourney API for AI-driven image generation. Additionally, it incorporates an AI upscaling API to adjust image resolutions for large print dimensions. Post-processing techniques such as format conversion and applying filters are then applied to enhance the final output. The result is an image ready for printing and downloading.

### Development Tools

Language: Python   
Library: requests, pillow   
GUI: gradio   
API: imagineapi.dev (Midjourney API), stability.ai (Upscaling API), ImgBB (Image Hosting API)   

### Image Size Calculation
Resolution: 
(65cm * 150cm) * 300dpi = 7677 * 17717 pixel
(50cm * 60cm) * 300dpi = 5906 * 8268 pixel
(65cm * 150cm) * 200dpi = 5118 * 11811 pixel
(50cm * 60cm) * 200dpi = 3937 * 4724 pixel

13:30 => (input) 674 * 1555 => (stability upscale) 1348 * 3110 => (pil upscale) 5118 * 11811
5:6 => (input) 935 * 1121 => (stability upscale) 1870 * 2242 => (pil upscale) 3937 * 4724

