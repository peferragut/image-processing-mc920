from skimage.draw import disk
import cv2 as cv
import numpy as np
import sys

def apply_fft(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    return f, fshift


def inverse_fft(shift_filter):
    filtered_img = np.abs(np.fft.ifft2(np.fft.ifftshift(shift_filter)))

    min_val = np.min(filtered_img)
    max_val = np.max(filtered_img)
    normalized_image = ((filtered_img - min_val) / (max_val - min_val)) * 255

    return normalized_image.astype(np.uint8)


def circle(height, width, radius):
    center = (height // 2, width // 2)
    rows, columns = disk(center, radius)
    return rows, columns


def low_pass(img, h, w, cutoff):
    lp_filter = np.zeros((h, w), dtype=np.complex128)
    fshift = apply_fft(img)[1]

    x, y = circle(h, w, cutoff)
    lp_filter[x, y] = fshift[x, y]

    filtered_img = inverse_fft(lp_filter)

    return filtered_img

    
def high_pass(img, h, w, cutoff):
    fshift = apply_fft(img)[1]
    x, y = circle(h, w, cutoff)
    fshift[x, y] = 0

    filtered_img = inverse_fft(fshift)

    return filtered_img


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
height = img.shape[0]
width = img.shape[1]
cutoff_freq = 70

low_pass_filter = low_pass(img, height, width, cutoff_freq)
high_pass_filter = high_pass(img, height, width, cutoff_freq)

cv.imshow("Low pass filter", low_pass_filter)
cv.imshow("High pass filter", high_pass_filter)

cv.waitKey(0)
cv.destroyAllWindows()

