import os
import cv2
from pdf2image import convert_from_path
folderPath = 'images'
ext = '.jpg'


def convertPDFtoImage(nameOfFile: str):
    newNameOfFile = nameOfFile[:-4] + ext
    pages = convert_from_path(nameOfFile)
    for i in range(len(pages)):
        pages[i].save(newNameOfFile, 'JPEG')
    return pages, newNameOfFile


def gaussian_blur(img: any):
    try:
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        return blur
    except FileNotFoundError as error:
        print(error)


def save_image(img: any, nameOfFile: str):
    totalFilePath = nameOfFile + ext
    try:
        os.mkdir(folderPath)
        totalFilePath = folderPath + '/' + totalFilePath
    except:
        totalFilePath = folderPath + '/' + totalFilePath

    print('Saving image output: ' + nameOfFile)
    cv2.imwrite(totalFilePath, img)
    print('Image saved!')


def show_image(img: any, nameOfWindow: str):
    cv2.imshow(nameOfWindow, img)  # Nome da janela, objeto imagem
    cv2.waitKey(0)
