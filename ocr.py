import pytesseract
import file_manager
import image_tools
import validation


def ocr_tesseract(img: any, nameOfFile: str):

    try:
        texto = pytesseract.image_to_string(img, lang='por')
        file_manager.save_textfile(texto, nameOfFile)
        return str(texto)
    except TypeError or FileNotFoundError as error:
        print(error)
        
        
def ocr_from_image(img, file_to_save):

    value = ocr_tesseract(img, 'output')
    if(validation.validate_output(value)):
        file_to_save.write('\n')
        file_to_save.write(value.lower())
    else:
        print('Could not extract value from', img) 
    