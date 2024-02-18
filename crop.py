import cv2
import json
import os
from pathlib import Path

image = cv2.imread("resources/btn_U.png")
RES_DIR = Path("debug_crop")
with open('box.json', newline='') as file:
    data = json.load(file)

if not os.path.isdir(RES_DIR):
    os.mkdir(RES_DIR)
    os.mkdir(RES_DIR / "stack_size")
    os.mkdir(RES_DIR / "bet_size")
    os.mkdir(RES_DIR / "btn")


PLAYERS_NAME = data["stack_ori"].keys()


# crop table 1
w, h = data["wh"][0], data["wh"][1]
x, y = data["ori"][0], data["ori"][1]
cropped_image = image[ y:y+h, x: x+w]
cv2.imwrite(f"{RES_DIR}/src.jpg", cropped_image)


# get stack size
for player in PLAYERS_NAME:
    w, h = data["stack_wh"][0], data["stack_wh"][1]
    x, y = data["stack_ori"][player][0], data["stack_ori"][player][1]
    cropped_image = image[ y:y+h, x : x+w]
    # Save the cropped image
    cv2.imwrite(f"{RES_DIR}/stack_size/{player}.jpg", cropped_image)

# get bet size
for player in PLAYERS_NAME:
    w, h = data["bet_wh"][0], data["bet_wh"][1]
    x, y = data["bet_ori"][player][0], data["bet_ori"][player][1]
    cropped_image = image[ y:y+h, x : x+w]
    # Save the cropped image
    cv2.imwrite(f"{RES_DIR}/bet_size/{player}.jpg", cropped_image)

# get pot size
w, h = data["pot_wh"][0], data["pot_wh"][1]
x, y = data["pot_ori"][0], data["pot_ori"][1]
cropped_image = image[ y:y+h, x : x+w]
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
    cropped_image = image[ y:y+h, x : x+w]
    cv2.imwrite(f"{RES_DIR}/btn/{player}.jpg", cropped_image)
"""
black: 22~25
btn: 72~75

is_btn:
cropped_image.mean() > 50
"""