#!/usr/bin/env node

// Example of using API4AI Image Upscale API.
const fs = require('fs')
const path = require('path')
const axios = require('axios').default
const FormData = require('form-data')

// Use 'normal' mode if you have an API Key from the API4AI Developer Portal. This is the method that users should normally prefer.
// Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
// For more details visit:
//   https://rapidapi.com/api4ai-api4ai-default/api/image-upscale/details
const MODE = 'normal'

// Your API4AI key. Fill this variable with the proper value if you have one.
const API4AI_KEY = ''

// Your RapidAPI key. Fill this variable with the proper value if you want
// to try api4ai via RapidAPI marketplace.
const RAPIDAPI_KEY = ''

const OPTIONS = {
  normal: {
    url: 'https://api4ai.cloud/image-upscale/v1/results',
    headers: { 'X-API-KEY': API4AI_KEY }
  },
  rapidapi: {
    url: 'https://image-upscale.p.rapidapi.com/v1/results',
    headers: { 'X-RapidAPI-Key': RAPIDAPI_KEY }
  }
}

// Parse args: path or URL to image.
const image = process.argv[2] || 'https://static.api4.ai/samples/image-upscale-1.png'

// Preapare request: form.
const form = new FormData()
if (image.includes('://')) {
  // Data from image URL.
  form.append('url', image)
} else {
  // Data from local image file.
  const fileName = path.basename(image)
  form.append('image', fs.readFileSync(image), fileName)
}

// Preapare request: headers.
const headers = {
  ...OPTIONS[MODE].headers,
  ...form.getHeaders(),
  'Content-Length': form.getLengthSync()
}

// Make request.
axios.post(OPTIONS[MODE].url, form, { headers })
  .then(function (response) {
    const responseEntities = response.data.results[0].entities
    const imgBase64 = Buffer
      .from(responseEntities[0].image, 'base64')
    const imgFormat = responseEntities[0].format.toLowerCase()

    fs.writeFile(`result.${imgFormat}`, imgBase64, () => {
      console.log(`💬 The "result.${imgFormat}" image is saved to the current directory.`)
    })
  })
