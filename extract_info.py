
import cv2
import json
import re
import os
import pytesseract

from pathlib import Path
def is_number(string):
    return string.replace(".", "").isnumeric()

CROP_DIR = Path("debug_crop")

with open('box.json', newline='') as file:
    data = json.load(file)

PLAYERS_NAME = data["stack_ori"].keys()

# checkout https://www.cnblogs.com/pyweb/p/11340357.html
image_to_string_cfg = "--psm 1" # 1 3 4 5 11 12
"""
Extract bet size
"""
for img_file in (CROP_DIR / "bet_size").rglob("*.jpg"):
    image = cv2.imread(str(img_file))
    results = pytesseract.image_to_string(image, config=image_to_string_cfg)
    try:
        if results == "":
            bb = ""
        else:
            bb = re.search(r'(.*?)BB', results).group(1).strip()
            assert(is_number(bb))
    except:
        breakpoint()
    with open(img_file.with_suffix('.txt'), "w") as f:
        f.write(bb)

"""
Extract stack size
"""
for img_file in (CROP_DIR / "stack_size").rglob("*.jpg"):
    image = cv2.imread(str(img_file))
    results = pytesseract.image_to_string(image, config=image_to_string_cfg)
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
    with open(img_file.with_suffix('.txt'), "w") as f:
        f.write(bb)

"""
Extract pot size
"""
image = cv2.imread(str(CROP_DIR/"pot.jpg"))
results =pytesseract.image_to_string(image, config=image_to_string_cfg)
bb = re.search(r':(.*?)BB', results).group(1).strip()
assert(is_number(bb))
with open( CROP_DIR/"pot.txt", "w") as f:
    f.write(bb)


"""
Extract btn position
"""
max_mean = 0
btn = None
for img_file in (CROP_DIR / "btn").rglob("*.jpg"):
    name = img_file.stem
    image = cv2.imread(str(img_file))
    m = image.mean()
    if m > max_mean:
        max_mean = m
        btn = name
with open( CROP_DIR/"btn.txt", "w") as f:
    f.write(btn)