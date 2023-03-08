import sys
import ocr
import numpy as np
import cv2  # OpenCV
import otsus_threshold as otsu
import qrcode
import img_utils
import qrcode


def main():
    args = sys.argv[1:]  # args is a list of the command line args
    if (len(args) == 0):
        print("Missing entry file. (i.e. 'example.pdf' or 'image.jpeg')")
        return

    if (args[0] == '--qrcode'):
        if (args[0][-4:] == '.pdf'):
            imgFile, imgName = img_utils.convertPDFtoImage(args[0])
            value = qrcode.read_qr_code(imgName)
            print(value)
            exit()
        else:
            value = qrcode.read_qr_code(args[1])
            print(value)
            exit()

    elif (args[0][-4:] == '.pdf'):
        imgFile, imgName = img_utils.convertPDFtoImage(args[0])
        # flag = 0 OR img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        img = cv2.imread(imgName, 0)
    else:
        # flag = 0 OR img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        img = cv2.imread(args[0], 0)

    ocr.ocr_tesseract(img, 'output')

    # reduce noise with Gaussian Blur
    blur = img_utils.gaussian_blur(img)
    ocr.ocr_tesseract(blur, 'gaussian_output')

    otsu_threshold, otsu_image = otsu.cv2otsu(blur)

    img_utils.save_image(otsu_image, 'otsu_image')
    ocr.ocr_tesseract(otsu_image, 'otsu_output')


main()
