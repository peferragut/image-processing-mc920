from math import ceil
import cv2 as cv
import numpy as np
import sys
    
def hide_message(img, bin_text, bit_planes):
    width = img.shape[1]
    height = img.shape[0]

    num_planes = len(bit_planes)
    msg_len = len(bin_text)

    img_len = width * height * 3
    img = np.reshape(img, img_len)

    max_bits = img_len * num_planes
    if msg_len > max_bits:
        msg_len = max_bits
        bin_text = bin_text[:msg_len]
        
    color_planes = ceil(msg_len / num_planes)

    mask = np.bitwise_or.reduce(1 << bit_planes)
    img[:color_planes] = img[:color_planes] & ~mask

    for plane_idx in range(num_planes):
        text_shifted_bitwise = bin_text[plane_idx::num_planes] << bit_planes[plane_idx]
        last_element_extension = np.zeros(color_planes - len(text_shifted_bitwise), dtype=np.uint8)
        text_shifted_bitwise = np.concatenate((text_shifted_bitwise, last_element_extension))
        img[:color_planes] = img[:color_planes] | text_shifted_bitwise

    img = np.reshape(img, (height, width, 3))


args = len(sys.argv)
if args != 5:
    err = "Too many arguments!" if args > 5 else "Not enough arguments!"
    print(err)
    print("Arguments required: program file, input image, input text file, bit planes and output image")
    sys.exit()
    

img = cv.imread(sys.argv[1])
bit_planes = np.array(list(sys.argv[3]), dtype=np.uint8)

text = open(sys.argv[2]).read() + '\0'
ascii_array = np.array([ord(char) for char in text], dtype=np.uint8)
bin_text = np.unpackbits(ascii_array)
hide_message(img, bin_text, bit_planes)

cv.imwrite(sys.argv[4], img)