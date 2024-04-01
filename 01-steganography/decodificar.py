import cv2 as cv
import numpy as np
import sys

def decode_msg(img):
    width = img.shape[1]
    height = img.shape[0]
    img = np.reshape(img, width * height * 3)
    px_lsb_array = img & 1
    packed_bits = np.packbits(px_lsb_array)

    null_array = np.where(packed_bits == 0)[0]
    delimiter_index = null_array[0] if len(null_array) > 0 else len(packed_bits)
    ascii_array = packed_bits[:delimiter_index]

    decoded_text = ascii_array.tobytes().decode("ascii")
    return decoded_text


args = len(sys.argv)
if args != 3:
    err = "Too many arguments!" if args > 3 else "Not enough arguments!"
    print(err)
    print("Arguments required: program file, output image and output text file")
    sys.exit()

img = cv.imread(sys.argv[1])
decoded_msg = decode_msg(img)

output_file = open(sys.argv[2], 'w')
output_file.write(decoded_msg)
output_file.close()


