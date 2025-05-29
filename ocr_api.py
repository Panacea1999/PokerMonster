import requests
import json
import numpy as np
import base64


def encode_image_to_base64(image_binary):
    image_array = np.asarray(bytearray(image_binary), dtype="uint8")
    image_bytes = image_array.tobytes()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return base64_image

image = open('/opt/tiger/haggsX/5.png', 'rb').read()
b64_frame = encode_image_to_base64(image)

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Pwd Here",
    "Content-Type": "application/json",
    "HTTP-Referer": "N/A",
    "X-Title": "N/A",
  },
  data=json.dumps({
    "model": "qwen/qwen2.5-vl-3b-instruct:free",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Extract and only answer the formatted ocr in this image"
          },
          {
            "type": "image_url",
            "image_url": {
            #   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
              "url": f"data:image/jpg;base64,{b64_frame}"
            }
          }
        ]
      }
    ],
    
  })
)

import sys
if response.status_code == 200:
    try:
        response_data = response.json()
        prediction = response_data["choices"][0]["message"]["content"].strip()
        print(prediction)
    except Exception as e:
        sys.stderr.write(f"{e}")