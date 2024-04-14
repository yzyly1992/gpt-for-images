import base64
import requests

def image_to_url(image_path: str) -> str:
    with open(image_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "TO BE ADDED",
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
        return res.json()