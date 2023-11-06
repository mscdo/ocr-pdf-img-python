import sys
import os
from os import listdir, wait
from os.path import isfile, join
import ocr
import numpy as np
import cv2  # OpenCV
import otsus_threshold as otsu
import qrcode
import img_utils
import file_utils
# from PIL import Image
import argparse
import matplotlib.pyplot as plt


def argParser():
    parser = argparse.ArgumentParser(description="OCR with Python")
    parser.add_argument("-qr", "--qrcode", action="store_true", help="files has qrcode to be read")
    # parser.add_argument('-p', '--pumpLink', action="store_true", help="Include PumpLink Name in F")
    group = parser.add_argument_group('Input Files', 'How multiple files are included. Type of files accepted: .jpg, .jpeg, .png')
    filesOptionsGroup = group.add_mutually_exclusive_group()
    filesOptionsGroup.add_argument("--files" , help="one or a list of files. (i.e. image.png image2.jpg)", nargs='+')
    filesOptionsGroup.add_argument("--folder", help="folder dir", nargs=1)
    # parser.add_argument('filename', nargs='+')
    # parser.print_help()
    return parser.parse_args()   


def withoutQrCodeImage(file, resize: float):
    # flag = 0 OR img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    img = cv2.imread(file, 0)

    # Resize image to its 60%
    imgresized = cv2.resize(img, None, fx=resize, fy=resize) 
    
    #Select ROI
    r = cv2.selectROI("SELECT AREA OF INTEREST", imgresized) 
    cv2.waitKey(0)
    # Cropped Image from ROI
    cropped_image = imgresized[int(r[1]):int(r[1]+r[3]),  
            int(r[0]):int(r[0]+r[2])] 
    
    
    cv2.imshow("CROPPED IMAGE", cropped_image) 
    cv2.waitKey(0)
    
    # Run Tesseract to OCR
    # print(str(text).lower())
    return ocr.ocr_tesseract(cropped_image, 'output')


def change_perspective(file):
    img = cv2.imread(file)
    assert img is not None, "file could not be read, check with os.path.exists()"
    rows,cols,ch = img.shape
    pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(300,300))
    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    plt.show()
    


def main():
   
    args =  argParser()    
    list_of_files = []
    print('------FILES INPUT------', '\n')
    if(args.folder and len(args.folder) == 1):
        print('Folder: ', args.folder[0], '\n')
        for filename in os.listdir(args.folder[0]):
            list_of_files.append(args.folder[0] + filename)
    elif(args.files and len(args.files) > 0):
        list_of_files = args.files
    
    for file in list_of_files:
        change_perspective(file)
    print('------EXTRACTING VALUES------ \n')
    # print(list_of_files, '\n')
    outputFile = open("output_device_numbers.txt","w+")
    
    if(False):
        if(len(list_of_files) >0):       
            for file in list_of_files:
                if (args.qrcode is True):
                    if (file[-4:] == '.pdf'):                    
                        try:
                            imgFile, imgName = img_utils.convertPDFtoImage(file)
                            value = qrcode.read_qr_code(file)
                        
                            if(value != 'None' and len(value) >0):
                                outputFile.write(value.lower())
                                outputFile.write('\n')
                            else:
                                text = withoutQrCodeImage(file, 0.6)
                                print('teste')
                                if(str(text) != 'None' and len(str(text)) > 0):
                                    outputFile.write(str(text).lower())
                                    outputFile.write('\n')
                                else:
                                    print('* Could not extract value from', file) 
                        except OSError:
                            print('Consider reviewing file name or path.')
                    else:
                        try:
                            value = qrcode.read_qr_code(file)
                            if(value and value != 'None' and len(value) >0):
                                outputFile.write(value.lower())
                                outputFile.write('\n')
                            else:
                                text = withoutQrCodeImage(file, 0.6)
                                
                                if(str(text).strip() != 'None' and len(str(text).strip()) > 0):
                                    outputFile.write(str(text).strip().lower())
                                    outputFile.write('\n')
                                else:
                                    print('* Could not extract value from', file) 
                        except OSError:
                            print('Consider reviewing file name or path')                
                        # file_utils.save_textfile(value, 'qrcode_value')
                # elif (file[-4:] == '.pdf'):
                #     imgFile, imgName = img_utils.convertPDFtoImage(file)
                #     # flag = 0 OR img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
                #     img = cv2.imread(imgName, 0)
                    
                else:
                    text = withoutQrCodeImage(file, 0.6)
                    if(str(text) != 'None' and len(str(text)) > 0):
                        print(str(text))
                        outputFile.write(str(text).lower())
                        outputFile.write('\n')
                    else:
                        print('* Could not extract value from', file)                    
                    
        outputFile.close()
        cv2.destroyAllWindows()


main()





    # if (args.qrcode==True):
    #     if (args.filename[-4:] == '.pdf'):
    #         imgFile, imgName = img_utils.convertPDFtoImage(args[0])
    #         value = qrcode.read_qr_code(imgName)
    #         print(value.lower())
    #         exit()
    #     else:
    #         value = qrcode.read_qr_code(args.filename[0])
    #         print(value.lower())
    #         # file_utils.save_textfile(value, 'qrcode_value')
    #         exit()

    # elif (args[0][-4:] == '.pdf'):
    #     imgFile, imgName = img_utils.convertPDFtoImage(args[0])
    #     # flag = 0 OR img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    #     img = cv2.imread(imgName, 0)
        
    # else:
    #     # flag = 0 OR img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    #     img = cv2.imread(args[0], 0)


    # ocr.ocr_tesseract(img, 'output')

    # otsu_threshold, otsu_image = otsu.cv2otsu(img)

    # # img_utils.save_image(otsu_image, 'otsu_image_without_blur')
    # texto = ocr.ocr_tesseract(otsu_image, 'otsu_output_without_blur')
    # print(texto.lower())


    # # reduce noise with Gaussian Blur
    # blur = img_utils.gaussian_blur(img)
    # # img_utils.save_image(blur, 'blur_image')
    # texto = ocr.ocr_tesseract(blur, 'gaussian_output')
    # print(texto.lower())



    # otsu_threshold, otsu_image = otsu.cv2otsu(blur)
    

    # # img_utils.save_image(otsu_image, 'otsu_image_with_blur')
    # texto = ocr.ocr_tesseract(otsu_image, 'otsu_output_with_blur')
    # print(texto.lower())


