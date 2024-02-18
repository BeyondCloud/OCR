import cv2
import json
import os
import numpy as np
from pathlib import Path
import shutil

target_image = "resources/all_bet.png"
image = cv2.imread(target_image)
image_gray = cv2.imread(target_image, 0)

RES_DIR = Path("debug_crop")
def pix2suit(pixel) -> str:
    if max(pixel) < 70:
        return "s"
    else:
        max_pixel = pixel.argmax()
        if max_pixel == 2: # R
            return "h"
        elif max_pixel == 1: # G
            return "c"
        elif max_pixel == 0: # B
            return "d"
    raise ValueError("Invalid pixel")

with open('box.json', newline='') as file:
    data = json.load(file)

if os.path.isdir(RES_DIR):
    shutil.rmtree(RES_DIR)
os.mkdir(RES_DIR)
os.mkdir(RES_DIR / "stack_size")
os.mkdir(RES_DIR / "bet_size")
os.mkdir(RES_DIR / "btn")
os.mkdir(RES_DIR / "board")
os.mkdir(RES_DIR / "hands")


PLAYERS_NAME = data["stack_ori"].keys()


# crop table 1
w, h = data["wh"][0], data["wh"][1]
x, y = data["ori"][0], data["ori"][1]
cropped_image = image[ y:y+h, x: x+w]
cv2.imwrite(f"{RES_DIR}/cropped.jpg", cropped_image)
ret, image_th = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite(f"{RES_DIR}/thres.jpg", image_th)



# get stack size
for player in PLAYERS_NAME:
    w, h = data["stack_wh"][0], data["stack_wh"][1]
    x, y = data["stack_ori"][player][0], data["stack_ori"][player][1]
    cropped_image = image_th[ y:y+h, x : x+w]
    # Save the cropped image
    cv2.imwrite(f"{RES_DIR}/stack_size/{player}.jpg", cropped_image)

# get bet size
for player in PLAYERS_NAME:
    w, h = data["bet_wh"][0], data["bet_wh"][1]
    x, y = data["bet_ori"][player][0], data["bet_ori"][player][1]
    cropped_image = image_th[ y:y+h, x : x+w]
    # Save the cropped image
    cv2.imwrite(f"{RES_DIR}/bet_size/{player}.jpg", cropped_image)

# get pot size
w, h = data["pot_wh"][0], data["pot_wh"][1]
x, y = data["pot_ori"][0], data["pot_ori"][1]
cropped_image = image_th[ y:y+h, x : x+w]
cv2.imwrite(f"{RES_DIR}/pot.jpg", cropped_image)


# check btn position
"""
w, h = data["btn_wh"][0], data["btn_wh"][1]
for player in PLAYERS_NAME:
    image = cv2.imread(f"resources/btn_{player}.png")
    x, y = data["btn_ori"][player][0], data["btn_ori"][player][1]
    cropped_image = image[ y:y+h, x : x+w]
    cv2.imwrite(f"{RES_DIR}/btn/{player}.jpg", cropped_image)
"""

# crop btn
w, h = data["btn_wh"][0], data["btn_wh"][1]
for player in PLAYERS_NAME:
    x, y = data["btn_ori"][player][0], data["btn_ori"][player][1]
    cropped_image = image_th[ y:y+h, x : x+w]
    cv2.imwrite(f"{RES_DIR}/btn/{player}.jpg", cropped_image)
"""
black: 22~25
btn: 72~75

is_btn:
cropped_image.mean() > 50
"""
# crop card
w,h = data["boardcard_wh"][0], data["boardcard_wh"][1]
for i, card in enumerate(data["board"]):
    x, y = card[0], card[1]
    suit = pix2suit(image[y,x])
    cropped_image = image_th[ y:y+h, x : x+w]
    if cropped_image.sum() == 0:
        continue
    cv2.imwrite(f"{RES_DIR}/board/{i}_{suit}.jpg", cropped_image)

# crop hands
w,h = data["hands_wh"][0], data["hands_wh"][1]
for i, card in enumerate(data["hands"]):
    x, y = card[0], card[1]
    suit = pix2suit(image[y,x])
    cropped_image = image_th[ y:y+h, x : x+w]
    cv2.imwrite(f"{RES_DIR}/hands/{i}_{suit}.jpg", cropped_image)
