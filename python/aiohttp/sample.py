#!/usr/bin/env python3

"""Example of using API4AI Image Upscale API."""

import asyncio
import base64
import os
import sys

import aiohttp


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


async def main():
    """Entry point."""
    image = sys.argv[1] if len(sys.argv) > 1 else 'https://static.api4.ai/samples/image-upscale-1.png'

    async with aiohttp.ClientSession() as session:
        if '://' in image:
            # Data from image URL.
            data = {'url': image}
        else:
            # Data from local image file.
            data = {'image': open(image, 'rb')}
        # Make request.
        async with session.post(OPTIONS[MODE]['url'],
                                data=data,
                                headers=OPTIONS[MODE].get('headers')) as response:
            resp_json = await response.json()

        image_format = resp_json['results'][0]['entities'][0]['format'].lower()
        img_b64 = resp_json['results'][0]['entities'][0]['image'].encode('utf8')

        path_to_image = os.path.join(f'result.{image_format}')
        with open(path_to_image, 'wb') as img:
            img.write(base64.decodebytes(img_b64))

        print(f'💬 The "result.{image_format}" image is saved to the current directory.')


if __name__ == '__main__':
    # Run async function in asyncio loop.
    asyncio.run(main())
