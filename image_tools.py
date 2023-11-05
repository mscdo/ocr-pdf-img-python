import os
import cv2
from pdf2image import convert_from_path
import numpy as np
import math


folderPath = 'images'
ext = '.jpg'

allowed_images_extensions = ['.jpg', '.jpeg', '.png']


def convertPDFtoImage(nameOfFile: str):
    newNameOfFile = nameOfFile[:-4] + ext
    pages = convert_from_path(nameOfFile)
    for i in range(len(pages)):
        pages[i].save(newNameOfFile, 'JPEG')
    return pages


def gaussian_blur(img: any):
    try:
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        return blur
    except FileNotFoundError as error:
        print(error)


def show_image(img: any, nameOfWindow: str):
    cv2.imshow(nameOfWindow, img)  # Nome da janela, objeto imagem
    cv2.waitKey(0)
    
    

def orientation_correction(img, save_image = False):
    # GrayScale Conversion for the Canny Algorithm  
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # Canny Algorithm for edge detection was developed by John F. Canny not Kennedy!! :)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    # Using Houghlines to detect lines
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
    
    # Finding angle of lines in polar coordinates
    angles = []
    for x1, y1, x2, y2 in lines[0]:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    
    # Getting the median angle
    median_angle = np.median(angles)
    
    # Rotating the image with this median angle
    img_rotated = ndimage.rotate(img, median_angle)
    
    if save_image:
        cv2.imwrite('orientation_corrected.jpg', img_rotated)
    return img_rotated
