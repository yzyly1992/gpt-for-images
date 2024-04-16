import base64
import requests
import argparse

def image_to_url(image_path: str) -> str:
    with open(image_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "c461ee306189279b7491884013bc1dd1",
            "image": base64.b64encode(file.read()),
        }
        try:
            res = requests.post(url, payload)
            json_res = res.json()
            if json_res["success"]:
                return json_res["data"]["url"]
            else:
                print(json_res)
                return None
        except Exception as e:
            print(e)
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, required=True)
    args = parser.parse_args()
    image_to_url(args.image_path)
    # image_path = "samples/the_last_of_us/11.jpg"
    # print(image_to_url(image_path))

# sample output
# {'data': {'id': 'PZkyvf0', 'title': '617f947ce49d', 'url_viewer': 'https://ibb.co/PZkyvf0', 'url': 'https://i.ibb.co/nspyN5t/617f947ce49d.jpg', 'display_url': 'https://i.ibb.co/bgtVM8D/617f947ce49d.jpg', 'width': 1920, 'height': 1080, 'size': 59620, 'time': 1713229958, 'expiration': 0, 'image': {'filename': '617f947ce49d.jpg', 'name': '617f947ce49d', 'mime': 'image/jpeg', 'extension': 'jpg', 'url': 'https://i.ibb.co/nspyN5t/617f947ce49d.jpg'}, 'thumb': {'filename': '617f947ce49d.jpg', 'name': '617f947ce49d', 'mime': 'image/jpeg', 'extension': 'jpg', 'url': 'https://i.ibb.co/PZkyvf0/617f947ce49d.jpg'}, 'medium': {'filename': '617f947ce49d.jpg', 'name': '617f947ce49d', 'mime': 'image/jpeg', 'extension': 'jpg', 'url': 'https://i.ibb.co/bgtVM8D/617f947ce49d.jpg'}, 'delete_url': 'https://ibb.co/PZkyvf0/17112c0840010813a4e41508ff3fa0a5'}, 'success': True, 'status': 200}