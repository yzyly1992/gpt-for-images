# pip install stability-sdk

import argparse
import os
import io
import warnings
from PIL import Image
import requests
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from dotenv import load_dotenv
load_dotenv()

size_dict_x1 = {
    # 0: (674, 1555),
    # 1: (935, 1121)

    0: (1555, 674),
    1: (1121, 935)
}

size_dict_x2 = {
    # 0: (5118, 11811),
    # 1: (3937, 4724)
    0: (11811, 5118),
    1: (4724, 3937)
}

stability_api = client.StabilityInference(
    key=os.environ.get("STABILITY_API_KEY"), # Your Stability API key.
    upscale_engine="esrgan-v1-x2plus", # The name of the upscaling model we want to use.
                                       # Available Upscaling Engines: esrgan-v1-x2plus
    verbose=True, # Print debug messages.
)

def resize_to_target_size(image, target_size):
    print("Resizing image to target size ...")
    # image = Image.open(image_path)
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    return image

def upscale_image(image_path, initial_size):
    print("Upscaling image using Stability AI ...")
    # check if image_path is url or local file
    if image_path.startswith("http"):
        img = Image.open(io.BytesIO(requests.get(image_path).content))
    else:
        img = Image.open(image_path)
    img = img.resize(initial_size)
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
                # big_img.save("samples/upscaled_image_x1.png")
                return big_img

def upscale_pipeline(image_path, target_size_index=0):
    upscale_x1 = upscale_image(image_path, size_dict_x1[target_size_index])
    upscale_x2 = resize_to_target_size(upscale_x1, size_dict_x2[target_size_index])
    # save upscaled image
    # upscale_x2.save("samples/upscaled_image_x2.png")
    return upscale_x2
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upscale an image to target size.")
    parser.add_argument("--image_path", type=str, help="Path or URL to the image to upscale.")
    parser.add_argument("--target_size_index", type=int, default=0, help="Index of target size to upscale to.")
    args = parser.parse_args()
    upscale_pipeline(args.image_path, args.target_size_index)