# image_generator.py
import os
import http.client
import json
import requests
from PIL import Image
import io
import time
import pprint

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
IMAGINE_API_URL = os.environ.get('IMAGINE_API_URL')
IMAGINE_API_TOKEN = os.environ.get('IMAGINE_API_TOKEN')

def send_request(method, path, body=None, headers={}):
    conn = http.client.HTTPSConnection(IMAGINE_API_URL.replace("http://", ""))
    conn.request(method, path, body=json.dumps(body) if body else None, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    conn.close()
    return data

def fetch_image(image_url):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        return image
    else:
        return f"Error: {response.status_code} - {response.text}"

def check_image_status(image_id):
    path = f"/items/images/{image_id}"
    headers = {
        'Authorization': f'Bearer {IMAGINE_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    while True:
        response_data = send_request('GET', path, headers=headers)
        if response_data['data']['status'] in ['completed', 'failed']:
            pprint.pp(response_data['data'])
            if response_data['data']['status'] == 'completed':
                image_url = response_data['data']['url']
                if image_url:
                    return fetch_image(image_url)
                else:
                    return "Error: Image URL not found in response."
            else:
                return "Error: Image generation failed."
        else:
            print(f"Image is not finished generating. Status: {response_data['data']['status']}")
            time.sleep(5)  # wait for 5 seconds before checking again
def generate_image_from_text(text):
    data = {
        "prompt": text
    }
    headers = {
        'Authorization': f'Bearer {IMAGINE_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    prompt_response_data = send_request('POST', '/items/images/', body=data, headers=headers)
    pprint.pp(prompt_response_data)
    image_id = prompt_response_data['data']['id']
    return check_image_status(image_id)

def generate_image_from_image(input_image):
    image_url = image_to_url(input_image)
    data = {
        "prompt": image_url
    }
    headers = {
        'Authorization': f'Bearer {IMAGINE_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    prompt_response_data = send_request('POST', '/items/images/', body=data, headers=headers)
    pprint.pp(prompt_response_data)
    image_id = prompt_response_data['data']['id']
    return check_image_status(image_id)

def generate_image_from_video(video):
    
    return check_image_status(image_id)