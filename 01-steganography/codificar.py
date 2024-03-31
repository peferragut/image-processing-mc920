import cv2 as cv
import sys

def hide_message(img, bin_text):
    bin_text += "00000000"
    data_len = len(bin_text)
    bit_idx = 0
    
    for row in img:
        for pixel in row:
            for rgb_word in range(3):
                if bit_idx == data_len:
                    return
                pixel[rgb_word] = pixel[rgb_word] & ~1 | int(bin_text[bit_idx])
                bit_idx += 1

img = cv.imread(sys.argv[1])

text = open(sys.argv[2]).read()
bin_text = ''.join(format(ord(char), '08b') for char in text)

hide_message(img, bin_text)

cv.imwrite("imagem_saida.png", img)