import cv2 as cv
from math import ceil

def insert_null(img, data_len):
    # define em qual elemento para
    # muda para 0 o lsb dos pŕóximos 8 elementos
    end_rgb = data_len % 3
    num_px = ceil(data_len / 3)

    num_rows = img.shape[1]
    num_col = img.shape[0]

    end_row = ceil(num_px / num_rows) - 1
    px_in_row = num_px - (end_row * num_col) - 1


def hide_message(img, bin_text):
    data_len = len(bin_text)
    bit_idx = 0
    for row in img:
        for pixel in row:
            for rgb_color in range(3):
                if bit_idx == data_len:
                    insert_null(img, data_len)
                    return
                pixel[rgb_color] = pixel[rgb_color] & ~1 | int(bin_text[bit_idx])
                bit_idx += 1

img = cv.imread("01-steganography/imagem_entrada.png")

text = open("01-steganography/texto_entrada.txt").read()
bin_text = ''.join(format(ord(char), '08b') for char in text)

hide_message(img, bin_text)

cv.imwrite("01-steganography/imagem_saida.png", img)