import sys
import json
import base64
import requests
import numpy as np


def encode_image_to_base64(image_binary):
    image_array = np.asarray(bytearray(image_binary), dtype="uint8")
    image_bytes = image_array.tobytes()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return base64_image

def inference_once(image_path, prompt_path):
  image = open(image_path, 'rb').read()
  b64_frame = encode_image_to_base64(image)
  with open(prompt_path, 'r') as f:
    prompt_txt = f.read()
    prompt_txt = prompt_txt.encode('utf-8').decode('unicode_escape')
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {AK}",
      "Content-Type": "application/json",
    },
    data=json.dumps({
      "model": "google/gemma-3-4b-it:free",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt_txt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpg;base64,{b64_frame}"
              }
            }
          ]
        }
      ],
      "temperature": 0.1,
    })
  )

  if response.status_code == 200:
      try:
          response_data = response.json()
          prediction = response_data["choices"][0]["message"]["content"].strip()
          return(prediction)
      except Exception as e:
          return f"Inf failed due to {e}"
  else:
    return f"Inf failed due to {response.json()}"
  

AK = "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"

# Demo cases

# [3h, 5h, 8h, 6c, 2d]
image_path = './PokerMonster/poker_demo_3h5h8h6c2d.png'
prompt_path = './PokerMonster/prompt/parse_cards.txt'
print(inference_once(image_path, prompt_path))

# [7s, 9s]
image_path = './PokerMonster/poker_demo_7s9s.png'
prompt_path = './PokerMonster/prompt/parse_cards.txt'
print(inference_once(image_path, prompt_path))

# dark_blue
image_path = './PokerMonster/fold_chips.png'
prompt_path = './PokerMonster/prompt/rec_dark_blue.txt'
print(inference_once(image_path, prompt_path))

# blue
image_path = './PokerMonster/active_chips.png'
prompt_path = './PokerMonster/prompt/rec_dark_blue.txt'
print(inference_once(image_path, prompt_path))

# 40
image_path = './PokerMonster/ocr_demo_40chips.png'
prompt_path = './PokerMonster/prompt/ocr.txt'
print(inference_once(image_path, prompt_path))