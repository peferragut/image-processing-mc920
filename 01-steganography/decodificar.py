import cv2 as cv
import numpy as np
import sys

def decode_msg(img, bit_planes):
    width = img.shape[1]
    height = img.shape[0]
    img = np.reshape(img, width * height * 3)

    extracted_planes = []

    for plane in bit_planes:
        extraction_plane = (img >> plane) & 1
        extracted_planes.append(extraction_plane)

    extracted_planes = np.array(extracted_planes)
    bit_planes_img = np.stack(extracted_planes).ravel('F')
    packed_bits = np.packbits(bit_planes_img)

    null_array = np.where(packed_bits == 0)[0]
    delimiter_index = null_array[0] if len(null_array) > 0 else len(packed_bits)
    ascii_array = packed_bits[:delimiter_index]

    decoded_text = ascii_array.tobytes().decode("ascii")
    return decoded_text

args = len(sys.argv)
if args != 4:
    err = "Too many arguments!" if args > 4 else "Not enough arguments!"
    print(err)
    print("Arguments required: program file, output image, bit planes and output text file")
    sys.exit()

img = cv.imread(sys.argv[1])
bit_planes = np.array(list(sys.argv[2]), dtype=np.uint8)

decoded_msg = decode_msg(img, bit_planes)

output_file = open(sys.argv[3], 'w')
output_file.write(decoded_msg)
output_file.close()
