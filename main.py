import os
import ocr
import numpy as np
import otsus_threshold as otsu
import qrcode
import validation, image_tools
import argparse



def arg_parser():
    parser = argparse.ArgumentParser(description="OCR with Python")
    parser.add_argument("-qr", "--qrcode", action="store_true", help="files has qrcode to be read")
    group = parser.add_argument_group('Input Files', 'How multiple files are included. Type of files accepted: .jpg, .jpeg, .png')
    filesOptionsGroup = group.add_mutually_exclusive_group()
    filesOptionsGroup.add_argument("--files" , help="one or a list of files. (i.e. image.png image2.jpg)", nargs='+')
    filesOptionsGroup.add_argument("--folder", help="folder dir", nargs=1)
    # parser.print_help()
    return parser.parse_args()  

def main():
   
    args =  arg_parser()
    list_of_files = []
    
    print('------FILES INPUT------', '\n')
    
    if(args.folder and len(args.folder) == 1):
        print('Folder: ', args.folder, '\n')
        for filename in os.listdir(args.folder[0]):
            list_of_files.append(args.folder[0] + filename)
    elif(args.files and len(args.files) > 0):
        list_of_files = args.files
    
    print('------EXTRACTING VALUES------ \n')
    # print(list_of_files, '\n')
    
    outputFile = open("output_device_numbers.txt","w+")
    
    if(len(list_of_files) >0):       
        for file in list_of_files:
            
            if (str(file)[-4:] == '.pdf'):       
                file = image_tools.convertPDFtoImage(file) # find ext of file            
            if (args.qrcode==True):
                try:
                    value = qrcode.read_qr_code(file)              
                    if(validation.validate_output(value)):
                        outputFile.write('\n')
                        outputFile.write(value.lower())
                    else:
                        print('Tentando extrair palavras na imagem.....')
                        ocr.ocr_from_image(file, outputFile)
                except OSError:
                    print('Error. Consider reviewing file name or path.')
            else:
                try:
                    ocr.ocr_from_image(file, outputFile)
                except OSError:
                    print('Error. Consider reviewing file name or path')                
                  
    outputFile.close()

main()
   