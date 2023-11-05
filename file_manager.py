import os
import cv2

folderPath = 'output'
ext = '.txt'

def save_image(img: any, nameOfFile: str):
    totalFilePath = folderPath + '/' + nameOfFile + ext
    print('-----------------')
    print('Saving image output: ' + nameOfFile)
    try:
        os.mkdir(folderPath)
        print('Creating folder ' + folderPath)
    except OSError as error:
        print('Dir already exists. Saving into dir...')

    cv2.imwrite(totalFilePath, img)
    print('Image saved!')
    print('-----------------')
    print('*****************')


def save_textfile(text: str, nameOfFile: str):
    totalFilePath = folderPath + '/' + nameOfFile + ext
    print('-----------------')
    print('Saving text output: ' + nameOfFile)
    try:
        os.mkdir(folderPath)
        print('Creating folder ' + folderPath)
    except OSError as error:
        print('Dir already exists. Saving into dir...')

    with open(totalFilePath, 'w') as f:
        print(text, file=f)  # Python 3.x
    print('File saved!')
    print('-----------------')
    print('*****************')
