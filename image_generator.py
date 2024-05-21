# https://docs.imagineapi.dev/quick-start/python
import json
import time
import http.client
import pprint
import dotenv
import os
dotenv.load_dotenv()
import argparse

url = "http://cl.imagineapi.dev/items/images/"
headers = {
    'Authorization': f'Bearer {os.getenv("IMAGINEAPI_KEY")}',
    'Content-Type': 'application/json'
}

image_ratio_dict = {
    0: '--ar 13:30',
    1: '--ar 5:6'
}

def send_request(method, path, body=None, headers={}):
    conn = http.client.HTTPSConnection("cl.imagineapi.dev")
    conn.request(method, path, body=json.dumps(body) if body else None, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    conn.close()
    return data
 
# def prompt_to_image(prompt: str):
#     data = {
#         "prompt": prompt
#     }
#     prompt_response_data = send_request('POST', '/items/images/', data, headers)
#     if 'error' in prompt_response_data:
#         print(f"Error: {prompt_response_data['error']}")
#         return None
#     return prompt_response_data.get('data').get('id')

# def image_to_image(url: str, prompt: str = ""):
#     data = {
#         "prompt": url + " " + prompt
#     }
#     prompt_response_data = send_request('POST', '/items/images/', data, headers)
#     if 'error' in prompt_response_data:
#         print(f"Error: {prompt_response_data['error']}")
#         return None
#     return prompt_response_data.get('data').get('id')

# def images_to_image(urls: list, prompt: str = ""):
#     data = {
#         "prompt": " ".join(urls) + " " + prompt
#     }
#     prompt_response_data = send_request('POST', '/items/images/', data, headers)
#     if 'error' in prompt_response_data:
#         print(f"Error: {prompt_response_data['error']}")
#         return None
#     return prompt_response_data.get('data').get('id')

def all_to_image(prompt: str, urls: list, target_size_index: int):
    prompt_content = " ".join(urls) + " " + prompt + " " + image_ratio_dict[target_size_index]
    data = {
        "prompt": prompt_content.strip()
    }
    prompt_response_data = send_request('POST', '/items/images/', data, headers)
    if 'error' in prompt_response_data:
        print(f"Error: {prompt_response_data['error']}")
        return None
    return prompt_response_data.get('data').get('id')
 
def check_image_status(id: str):
    response_data = send_request('GET', f"/items/images/{id}", headers=headers)
    if response_data['data']['status'] in ['completed', 'failed']:
        print('Completed image details',)
        pprint.pp(response_data['data'])
        return True
    else:
        print(f"Image is not finished generation. Status: {response_data['data']['status']}")
        return False

def loop_check_status(id: str):
    while not check_image_status(id):
        time.sleep(5)  # wait for 5 seconds
    return True

def get_image_urls(id: str):
    response_data = send_request('GET', f"/items/images/{id}", headers=headers)
    if response_data['data']['status'] == 'completed':
        return response_data['data']['upscaled_urls']
    else:
        return None

def image_gen_pipeline(prompt: str = '', urls: list = [], target_size_index: int = 0):
    if (prompt == '' and len(urls) == 0):
        raise ValueError("Either prompt or urls should be provided")
    id = all_to_image(prompt, urls, target_size_index)
    loop_check_status(id)
    return get_image_urls(id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate image from prompt')
    parser.add_argument('--prompt', type=str, default='', help='Prompt for image generation')
    parser.add_argument('--urls', nargs='+', default=[], help='List of urls to generate image from')
    parser.add_argument('--target_size_index', type=int, default=0, help='Index of target size to generate image')
    args = parser.parse_args()
    print(image_gen_pipeline(args.prompt, args.urls, args.target_size_index))

# prompt to image result
# Image is not finished generation. Status: in-progress
# Image is not finished generation. Status: in-progress
# Image is not finished generation. Status: in-progress
# Completed image details
# {'id': '29d35f68-d55f-47dc-b3fe-cb0cb3ea0b0c',
#  'prompt': 'A beautiful sunset over the ocean --ar 13:30 --chaos 40 --stylize '
#            '1000',
#  'results': 'fc306264-9da9-4c9c-adcf-40efea90cb29',
#  'user_created': 'bff27409-151b-45d5-a97d-f20448df33fb',
#  'date_created': '2024-05-15T15:33:38.319Z',
#  'status': 'completed',
#  'progress': None,
#  'url': 'https://cl.imagineapi.dev/assets/fc306264-9da9-4c9c-adcf-40efea90cb29/fc306264-9da9-4c9c-adcf-40efea90cb29.png',
#  'error': None,
#  'upscaled_urls': ['https://cl.imagineapi.dev/assets/5133f1fe-2bbc-4868-b000-fae07a3e8c0e/5133f1fe-2bbc-4868-b000-fae07a3e8c0e.png',
#                    'https://cl.imagineapi.dev/assets/ea5b99ef-600d-4ce6-9aeb-056f4e2fcbd4/ea5b99ef-600d-4ce6-9aeb-056f4e2fcbd4.png',
#                    'https://cl.imagineapi.dev/assets/2e3c28f0-5e3c-44d8-9fbc-47e634bf2fd6/2e3c28f0-5e3c-44d8-9fbc-47e634bf2fd6.png',
#                    'https://cl.imagineapi.dev/assets/56c224db-8fdb-4baa-baf4-4184409ce08e/56c224db-8fdb-4baa-baf4-4184409ce08e.png'],
#  'ref': None,
#  'upscaled': ['2e3c28f0-5e3c-44d8-9fbc-47e634bf2fd6',
#               '5133f1fe-2bbc-4868-b000-fae07a3e8c0e',
#               '56c224db-8fdb-4baa-baf4-4184409ce08e',
#               'ea5b99ef-600d-4ce6-9aeb-056f4e2fcbd4']}

# images to image result
# Image is not finished generation. Status: in-progress
# Image is not finished generation. Status: in-progress
# Completed image details
# {'id': 'c2c3df60-0dee-4602-bf37-605ff1573891',
#  'prompt': 'https://cl.imagineapi.dev/assets/ea5b99ef-600d-4ce6-9aeb-056f4e2fcbd4/ea5b99ef-600d-4ce6-9aeb-056f4e2fcbd4.png '
#            'https://cl.imagineapi.dev/assets/2e3c28f0-5e3c-44d8-9fbc-47e634bf2fd6/2e3c28f0-5e3c-44d8-9fbc-47e634bf2fd6.png '
#            'A beautiful sunset over the ocean --ar 13:30 --chaos 40 --stylize '
#            '500',
#  'results': 'faba29bb-810e-4a08-af5c-b48936d34faa',
#  'user_created': 'bff27409-151b-45d5-a97d-f20448df33fb',
#  'date_created': '2024-05-15T15:48:11.573Z',
#  'status': 'completed',
#  'progress': None,
#  'url': 'https://cl.imagineapi.dev/assets/faba29bb-810e-4a08-af5c-b48936d34faa/faba29bb-810e-4a08-af5c-b48936d34faa.png',
#  'error': None,
#  'upscaled_urls': ['https://cl.imagineapi.dev/assets/71f4b2d8-7d3b-4c83-9ccb-25b67c3ffc55/71f4b2d8-7d3b-4c83-9ccb-25b67c3ffc55.png',
#                    'https://cl.imagineapi.dev/assets/185ad9c1-74c0-4789-bf9f-914eab39faee/185ad9c1-74c0-4789-bf9f-914eab39faee.png',
#                    'https://cl.imagineapi.dev/assets/62205ff8-0ec1-4d95-b8d8-2a68a58b4151/62205ff8-0ec1-4d95-b8d8-2a68a58b4151.png',
#                    'https://cl.imagineapi.dev/assets/489904a3-0820-4f3d-af7d-ab3d1016ca0e/489904a3-0820-4f3d-af7d-ab3d1016ca0e.png'],
#  'ref': None,
#  'upscaled': ['185ad9c1-74c0-4789-bf9f-914eab39faee',
#               '489904a3-0820-4f3d-af7d-ab3d1016ca0e',
#               '62205ff8-0ec1-4d95-b8d8-2a68a58b4151',
#               '71f4b2d8-7d3b-4c83-9ccb-25b67c3ffc55']}

# # the other dimension
# Image is not finished generation. Status: in-progress
# Image is not finished generation. Status: in-progress
# Completed image details
# {'id': '57a47169-e405-4d8e-bba3-0bc71e5add49',
#  'prompt': 'diamond and pink liquid, rendering style --ar 5:6',
#  'results': '27c412b6-0c24-40e8-b74d-120d455b6a89',
#  'user_created': 'bff27409-151b-45d5-a97d-f20448df33fb',
#  'date_created': '2024-05-21T22:02:47.299Z',
#  'status': 'completed',
#  'progress': None,
#  'url': 'https://cl.imagineapi.dev/assets/27c412b6-0c24-40e8-b74d-120d455b6a89/27c412b6-0c24-40e8-b74d-120d455b6a89.png',
#  'error': None,
#  'upscaled_urls': ['https://cl.imagineapi.dev/assets/41145610-a4a1-460c-8155-7d18c90a3f56/41145610-a4a1-460c-8155-7d18c90a3f56.png',
#                    'https://cl.imagineapi.dev/assets/82281fd1-8baf-4978-b614-bdb3c8950e1d/82281fd1-8baf-4978-b614-bdb3c8950e1d.png',
#                    'https://cl.imagineapi.dev/assets/374043c0-1bd6-46d3-a828-fad18cdd2568/374043c0-1bd6-46d3-a828-fad18cdd2568.png',
#                    'https://cl.imagineapi.dev/assets/8fe32eef-c1e9-4baf-8018-7f183508910a/8fe32eef-c1e9-4baf-8018-7f183508910a.png'],
#  'ref': None,
#  'upscaled': ['374043c0-1bd6-46d3-a828-fad18cdd2568',
#               '41145610-a4a1-460c-8155-7d18c90a3f56',
#               '82281fd1-8baf-4978-b614-bdb3c8950e1d',
#               '8fe32eef-c1e9-4baf-8018-7f183508910a']}