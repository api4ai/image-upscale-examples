#!/usr/bin/env python3

"""Example of using API4AI Image Upscale API."""

import base64
import os
import sys

import requests


# Use 'normal' mode if you have an API Key from the API4AI Developer Portal. This is the method that users should normally prefer.
#
# Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
# For more details visit:
#   https://rapidapi.com/api4ai-api4ai-default/api/image-upscale/details
MODE = 'normal'

# Your API4AI key. Fill this variable with the proper value if you have one.
API4AI_KEY = ''

# Your RapidAPI key. Fill this variable with the proper value if you want
# to try api4ai via RapidAPI marketplace.
RAPIDAPI_KEY = ''


OPTIONS = {
    'normal': {
        'url': 'https://api4ai.cloud/image-upscale/v1/results',
        'headers': {'X-API-KEY': API4AI_KEY}
    },
    'rapidapi': {
        'url': 'https://image-upscale.p.rapidapi.com/v1/results',
        'headers': {'X-RapidAPI-Key': RAPIDAPI_KEY}
    }
}


if __name__ == '__main__':
    # Parse args.
    image = sys.argv[1] if len(sys.argv) > 1 else 'https://static.api4.ai/samples/image-upscale-1.png'

    if '://' in image:
        # POST image via URL.
        response = requests.post(
            OPTIONS[MODE]['url'],
            headers=OPTIONS[MODE].get('headers'),
            data={'url': image})
    else:
        # POST image as file.
        with open(image, 'rb') as image_file:
            response = requests.post(
                OPTIONS[MODE]['url'],
                headers=OPTIONS[MODE].get('headers'),
                files={'image': (os.path.basename(image), image_file)}
            )

    response_entities = response.json()['results'][0]['entities']
    image_format = response_entities[0]['format'].lower()
    img_b64 = response_entities[0]['image'].encode('utf8')

    path_to_image = os.path.join(f'result.{image_format}')
    with open(path_to_image, 'wb') as img:
        img.write(base64.decodebytes(img_b64))

    print(f'💬 The "result.{image_format}" image is saved to the current directory.')
