import cv2 as cv

def decode_msg(img):
    curr_word = bin_text = ''
    for row in img:
        for pixel in row:
            for rgb_word in pixel:
                if len(curr_word) == 8:
                    bin_text += curr_word
                    if curr_word == "00000000":
                        return bin_text
                    curr_word = ''
                curr_word += str(rgb_word & 1)
            
img = cv.imread("01-steganography/imagem_saida.png")
decoded_msg = decode_msg(img)

bin_chars = [decoded_msg[i:i + 8] for i in range(0, len(decoded_msg) - 8, 8)]
text = ''
for bin_char in bin_chars:
    ascii_num = int(bin_char, 2)
    char = chr(ascii_num)
    text += char

print(text)

