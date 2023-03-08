import pytesseract
import file_utils


def ocr_tesseract(img: any, nameOfFile: str):

    try:
        texto = pytesseract.image_to_string(img, lang='por')
        file_utils.save_textfile(texto, nameOfFile)
        return texto
    except TypeError or FileNotFoundError as error:
        print(error)
        exit()
