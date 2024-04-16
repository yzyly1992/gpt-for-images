# pip install stability-sdk

import argparse
import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
os.environ['STABILITY_KEY'] = 'key-goes-here'

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    upscale_engine="esrgan-v1-x2plus", # The name of the upscaling model we want to use.
                                       # Available Upscaling Engines: esrgan-v1-x2plus
    verbose=True, # Print debug messages.
)

def resize_to_target_size(image_path, target_size):
    print("Resizing image to target size ...")
    image = Image.open(image_path)
    image = image.resize(target_size, Image.ANTIALIAS)
    return image

def upscale_image(image_path, output_path):
    print("Upscaling image using Stability AI ...")
    img = Image.open(image_path)
    answers = stability_api.upscale(
        init_image=img, # Pass our image to the API and call the upscaling process.
        # width=1024, # Optional parameter to specify the desired output width.
    )
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please submit a different image and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                big_img = Image.open(io.BytesIO(artifact.binary))
                big_img.save(output_path) # Save our image to a local file.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upscale an image to target size.")
    parser.add_argument("--image_path", type=str, help="Path to the image to upscale.")
    parser.add_argument("--target_size", type=int, nargs='+', help="Target size for the image.")
    args = parser.parse_args()
    upscale_image(args.image_path, "upscaled_image.png")
    resize_to_target_size("upscaled_image.png", tuple(args.target_size))
    print("Image upscaled and resized successfully!")