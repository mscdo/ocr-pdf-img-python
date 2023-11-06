import pytesseract
import file_utils


def ocr_tesseract(img, nameOfFile: str):
  
    try:
        texto = pytesseract.image_to_string(img, lang='por')
        # file_utils.save_textfile(texto, nameOfFile)
        return str(texto)
    except TypeError or FileNotFoundError as error:
        print(error)
  
