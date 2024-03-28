import cv2 as cv

def hide_message(img, bin_text):
    bin_text += "00000000"
    data_len = len(bin_text)
    bit_idx = 0
    
    for row in img:
        for pixel in row:
            for rgb_color in range(3):
                if bit_idx == data_len:
                    return
                pixel[rgb_color] = pixel[rgb_color] & ~1 | int(bin_text[bit_idx])
                bit_idx += 1

img = cv.imread("01-steganography/imagem_entrada.png")

text = open("01-steganography/texto_entrada.txt").read()
bin_text = ''.join(format(ord(char), '08b') for char in text)

hide_message(img, bin_text)

cv.imwrite("01-steganography/imagem_saida.png", img)