
import cv2
import json
import re
import os
import pytesseract

from pathlib import Path
def is_number(string):
    return string.replace(".", "").isnumeric()

CROP_DIR = Path("debug_crop")
extracted_info = {}

with open('box.json', newline='') as file:
    data = json.load(file)

PLAYERS_NAME = data["stack_ori"].keys()

# checkout https://www.cnblogs.com/pyweb/p/11340357.html
"""
  0 Orientation and script detection (OSD) only.
  1 Automatic page segmentation with OSD.
  2 Automatic page segmentation, but no OSD, or OCR.
  3 Fully automatic page segmentation, but no OSD. (Default)
  4 Assume a single column of text of variable sizes.
  5 Assume a single uniform block of vertically aligned text.
  6 Assume a single uniform block of text.
  7 Treat the image as a single text line.
  8 Treat the image as a single word.
  9 Treat the image as a single word in a circle.
  10 Treat the image as a single character.
  11 Sparse text. Find as much text as possible in no particular order.
  12 Sparse text with OSD.
  13 Raw line. Treat the image as a single text line,
"""

CFG_STR = "--psm 1" # 1 3 4 5 11 12
CFG_CHR = "--psm 9" # 8 9 13  : 8 13 bad result
"""
Extract bet size
"""
bets = {}
for img_file in (CROP_DIR / "bet_size").rglob("*.jpg"):
    who = img_file.stem
    image = cv2.imread(str(img_file))
    results = pytesseract.image_to_string(image, config=CFG_STR)
    bb = ""
    try:
        if results != "":
            bb = re.search(r'(.*?)BB', results).group(1).strip()
            assert(is_number(bb))
    except:
        breakpoint()
    bets[who] = bb

extracted_info["bets"] = bets


"""
Extract stack size
"""
stacks = {}
for img_file in (CROP_DIR / "stack_size").rglob("*.jpg"):
    who = img_file.stem
    image = cv2.imread(str(img_file))
    results = pytesseract.image_to_string(image, config=CFG_STR)
    results = results.replace("\n"," ")
    try:
        if results == "":
            bb = ""
        elif "All" in results:
            bb = "All-in"
        elif "Sit" in results:
            bb = "Sitting Out"
        else:
            bb = re.search(r'(.*?)BB', results).group(1).strip()
            assert(is_number(bb))
    except:
        breakpoint()
    stacks[who] = bb
extracted_info["stacks"] = stacks


"""
Extract pot size
"""
image = cv2.imread(str(CROP_DIR/"pot.jpg"))
results =pytesseract.image_to_string(image, config=CFG_STR)
bb = re.search(r':(.*?)BB', results).group(1).strip()
assert(is_number(bb))
extracted_info["pot"] = bb

"""
Extract btn position
"""
max_sum = 0
btn = None
for img_file in (CROP_DIR / "btn").rglob("*.jpg"):
    name = img_file.stem
    image = cv2.imread(str(img_file))
    m = image.sum()
    if m > max_sum:
        max_sum = m
        btn = name
extracted_info["btn"] = btn

"""
Extract board
"""
board = []
for img_file in sorted((CROP_DIR / "board").rglob("*.jpg")):
    image = cv2.imread(str(img_file))
    suit = img_file.stem.split("_")[-1]
    results = pytesseract.image_to_string(image, config=CFG_CHR).strip()
    if results == "":
        continue
    else:
        board.append( f"{results}{suit}")

extracted_info["board"] = board

"""
Extract hards
"""
hands = []
for img_file in sorted((CROP_DIR / "hands").rglob("*.jpg")):
    image = cv2.imread(str(img_file))
    suit = img_file.stem.split("_")[-1]
    results = pytesseract.image_to_string(image, config=CFG_CHR).strip()
    if results == "":
        continue
    else:
        hands.append( f"{results}{suit}")
extracted_info["hands"] = hands

with open(CROP_DIR / "info.json", 'w') as f:
    json.dump(extracted_info, f, indent=4)