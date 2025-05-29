import requests
import json
import numpy as np

response = requests.post(
  url="http://localhost:8000/v1/chat/completions",
  headers={
    "Content-Type": "application/json"
  },
  data=json.dumps({
    "model": "google/gemma-3-4b-it",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": """[TABLE_CONFIGURATION]
BTN=P2
SB=P3 0.5BB
BB=P4 1BB

[STACKS]
P1: 20.8BB
P2: 23.4BB [Kc 8c]
P3: 32.7BB
P4: 83.2BB
P5: 56.1BB
POT=1.5BB

[PREFLOP]
P5: FOLD
P1: FOLD
P2: RAISE 2BB
P3: CALL 1BB
P4: CALL 1BB

[STACKS]
P2: 21.4BB [Kc 8c]
P3: 31.2BB
P4: 82.2BB
POT=6.0BB

[FLOP][4d 7d Ah]
P3: CHECK
P4: CHECK
P2:"""
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