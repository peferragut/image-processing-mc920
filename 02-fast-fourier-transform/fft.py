import cv2 as cv
import numpy as np
import sys

def low_pass():
    pass

def high_pass():
    pass

def band_pass():
    pass

def band_stop():
    pass

args = len(sys.argv)
if args != 2:
    err = "Too many arguments! Only the input image path is needed." if args > 2 else "Missing image path!"
    print(err)
    sys.exit()
    
img = cv.imread(sys.argv[1], 0)

f = np.fft.fft2(img)
fshift = np.fft.fftshift(f) # center freq spectrum
