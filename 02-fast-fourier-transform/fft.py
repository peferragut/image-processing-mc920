from skimage.draw import disk
import cv2 as cv
import numpy as np
import sys
import matplotlib.pyplot as plt

def apply_fft(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    freq_mag = 20 * np.log(np.abs(fshift))
    return freq_mag, fshift


def inverse_fft(shift_filter):
    filtered_img = np.abs(np.fft.ifft2(np.fft.ifftshift(shift_filter)))

    min_val = np.min(filtered_img)
    max_val = np.max(filtered_img)
    normalized_image = ((filtered_img - min_val) / (max_val - min_val)) * 255

    return normalized_image.astype(np.uint8)


def circle(h, w, radius):
    center = (h // 2, w // 2)
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


def band_pass(img, h, w, ini_cutoff, end_cutoff):
    bp_filter = np.zeros((h, w), dtype=np.complex128)
    fshift = apply_fft(img)[1]

    x2, y2 = circle(h, w, end_cutoff)
    bp_filter[x2, y2] = fshift[x2, y2]

    x1, y1 = circle(h, w, ini_cutoff)
    bp_filter[x1, y1] = 0

    filtered_img = inverse_fft(bp_filter)
    return filtered_img


def band_stop(img, h, w, ini_cutoff, end_cutoff):
    fshift = apply_fft(img)[1]
    copy = fshift.copy()
    
    x2, y2 = circle(h, w, end_cutoff)
    fshift[x2, y2] = 0

    x1, y1 = circle(h, w, ini_cutoff)
    fshift[x1, y1] = copy[x1, y1]

    filtered_img = inverse_fft(fshift)
    return filtered_img


args = len(sys.argv)
if args != 2:
    err = "Too many arguments! Only the input image path is needed." if args > 2 else "Missing image path!"
    print(err)
    sys.exit()
    
img = cv.imread(sys.argv[1], 0)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.hist(img.flatten(), bins=256, range=(0, 255), color='blue', alpha=0.6)
plt.title('Histogram of Original Image')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

height = img.shape[0]
width = img.shape[1]

cutoff = 70

low_pass_filter = low_pass(img, height, width, cutoff)
cv.imwrite("low_pass_img.png", low_pass_filter)

high_pass_filter = high_pass(img, height, width, cutoff)
cv.imwrite("high_pass_img.png", high_pass_filter)

cutoff_ini = 40
cutoff_end = 130

band_pass_filter = band_pass(img, height, width, cutoff_ini, cutoff_end)
cv.imwrite("band_pass_img.png", band_pass_filter)

band_stop_filter = band_stop(img, height, width, cutoff_ini, cutoff_end)
cv.imwrite("band_stop_img.png", band_stop_filter)


# Compression
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
mag = 20 * np.log(np.abs(fshift))
compressed_freq = np.where(mag < 260, 0, fshift)
compressed_img = np.abs(np.fft.ifft2(np.fft.ifftshift(compressed_freq)))

cv.imwrite("compressed_img.png", compressed_img.astype(np.uint8))

plt.subplot(1, 2, 2)
plt.hist(compressed_img.flatten(), bins=256, range=(0, 255), color='green')
plt.title('Histogram of Compressed Image')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.show()