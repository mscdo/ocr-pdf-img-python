import cv2
import numpy as np
import ocr

# Load image, grayscale, Gaussian blur, Otsu's threshold
img_raw = cv2.imread('./test/assets/pivo.jpeg')
roi = cv2.selectROI(img_raw)
print(roi)
roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

#show cropped image
# cv2.imshow("ROI", roi_cropped)

cv2.imwrite("crop.jpeg",roi_cropped)
img_raw = cv2.imread('crop.jpeg')
texto = ocr.ocr_tesseract(img_raw, 'roi_cropped')


#hold window
# cv2.waitKey(0)