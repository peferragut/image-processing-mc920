import cv2 as cv
import numpy as np
import sys

def hide_message(img, bin_text):
    width = img.shape[1]
    height = img.shape[0]
    msg_len = len(bin_text)
    img_len = width * height * 3
    img = np.reshape(img, img_len)

    if msg_len > img_len:
        bin_text = bin_text[:img_len]

    img[:msg_len] = img[:msg_len] & ~1 | bin_text
    img = np.reshape(img, (height, width, 3))

args = len(sys.argv)
if args != 4:
    err = "Too many arguments!" if args > 4 else "Not enough arguments!"
    print(err)
    print("Arguments required: program file, input image and input text file")
    sys.exit()

img = cv.imread(sys.argv[1])

text = open(sys.argv[2]).read() + '\0'
ascii_array = np.array([ord(char) for char in text], dtype=np.uint8)
bin_text = np.unpackbits(ascii_array)
hide_message(img, bin_text)

cv.imwrite(sys.argv[3], img)