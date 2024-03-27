# converter cada caractere da mensagem para sua palavra binária correspondente
# alterar os bits menos significativos da imagem com os bits da mensagem

import cv2 as cv
import numpy as np
from pathlib import Path


img = cv.imread("01-steganography/imagem_entrada.png")

text = open("01-steganography/texto_entrada.txt").read()
bin_text = ''.join(format(ord(char), '08b') for char in text)
data_len = len(bin_text)

m = img.shape[0]
n = img.shape[1]
