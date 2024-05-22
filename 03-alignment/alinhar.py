import cv2 as cv
import numpy as np
from scipy.ndimage import rotate 
import sys

THRESH = 180

def proj_obj_fun(projection):
    # It calculates the sum of the square 
    diff = np.diff(projection)
    sum_square_diff = np.sum(diff ** 2)
    return sum_square_diff

def horizontal_projection(img):
    bin_img = cv.threshold(img, THRESH, 255, cv.THRESH_BINARY)[1]
    
    angle = 0
    max_sum = -np.inf
    for i in range(-90, 91):
        rotated_img = rotate(bin_img, i, reshape=False)
        projection = np.sum(rotated_img, axis=1)
        curr_sum = proj_obj_fun(projection)
        if curr_sum > max_sum:
            max_sum = curr_sum
            angle = i
    aligned_img = rotate(img, angle, reshape=False, cval=255)
    return angle, aligned_img

def hough_transform(img):
    bin_img = cv.threshold(img, THRESH, 255, cv.THRESH_BINARY)[1]
    borders = cv.Canny(bin_img, 50, 150)
    lines = cv.HoughLines(borders, 1, np.pi / 180, 200)

    if lines is None:
        borders = cv.Laplacian(bin_img, cv.CV_64F).astype(np.uint8)
        lines = cv.HoughLines(borders, 1, np.pi / 180, 200)

    thetas = lines[:, :, -1]
    angle_idx, counts = np.unique(np.round(np.degrees(thetas)), return_counts=True)
    most_freq_angle = angle_idx[np.argmax(counts)]
    angle = most_freq_angle - 90

    aligned_img = rotate(img, angle, reshape=False, cval=255)

    return angle, aligned_img


errors = {
    0: "Too many arguments! Only the input image path is needed.",
    1: "Missing image path!",
    2: "Given input path is not from a PNG file!",
    3: "Output path is not from a PNG file!",
    4: "Invalid mode. You can choose between Horizontal Projection (0) or Hough Transform (1)"
}

# Checking command line errors
args = len(sys.argv)
err = None

if args != 4:
    err = errors[0] if args > 4 else errors[1]

elif not sys.argv[1].endswith('.png'):
    err = errors[2]

elif not sys.argv[3].endswith('.png'):
    err = errors[3]

elif not sys.argv[2] in ["0", "1"]:
    err = errors[4]

if err is not None:
    print(err)
    sys.exit()


img = cv.imread(sys.argv[1], 0)

angle = ''
aligned_img = ''

if sys.argv[2] == "0":
    angle, aligned_img = horizontal_projection(img)
elif sys.argv[2] == "1":
    angle, aligned_img = hough_transform(img)

print("Correction Angle:", angle, "degrees")
cv.imwrite(sys.argv[3], aligned_img)
