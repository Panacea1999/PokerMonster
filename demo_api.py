import requests
import json
import numpy as np
import base64


def encode_image_to_base64(image_binary):
    image_array = np.asarray(bytearray(image_binary), dtype="uint8")
    image_bytes = image_array.tobytes()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return base64_image

image = open('/opt/tiger/haggsX/PokerMonster/poker_demo_3h5h8h6c2d.png', 'rb').read()
# image = open('/opt/tiger/haggsX/PokerMonster/poker_demo_7s9s.png', 'rb').read()
# image = open('/opt/tiger/haggsX/PokerMonster/name_demo_gray.png', 'rb').read()
b64_frame = encode_image_to_base64(image)

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
    "HTTP-Referer": "N/A",
    "X-Title": "N/A",
  },
  data=json.dumps({
    "model": "google/gemma-3-4b-it:free",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            # 识别文字和数字
            # "text": "Extract and only answer the formatted ocr in this image"
            # 识别是否有弃牌
            # "text": "Does the image contain fold or 弃牌, answer Yes or No"
            # 识别扑克牌
            "text": """Is there any playing card in the image? If so, please identify the rank and suit of each card.
            s means spades, h means heart, d means diamond, c means club.
            For example, represent the seven of diamonds and the king of spades as '7d' and 'Ks' by answering [7d, Ks]."""
            # 识别灰名
            # "text": """Assume you are determining whether the text color is white or gray based on its brightness.  
# If the brightness is close to pure white (#FFFFFF), answer 'white'.  
# If it is slightly darker, such as a light gray (#BBBBBB or #AAAAAA), answer 'gray'.  
# Respond with 'white' or 'gray' only."""
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
    "temperature": 1,
    "top_p": 1,
  })
)

import sys
print(response.json())
if response.status_code == 200:
    try:
        response_data = response.json()
        prediction = response_data["choices"][0]["message"]["content"].strip()
        print(prediction)
    except Exception as e:
        sys.stderr.write(f"{e}")