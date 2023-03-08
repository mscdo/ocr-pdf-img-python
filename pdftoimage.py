from pdf2image import convert_from_path


def convertPDFtoImage(nameOfFile: str):
    pages = convert_from_path(nameOfFile)
    for i in range(len(pages)):
        pages[i].save(nameOfFile[:-4] + '.jpg', 'JPEG')
    return pages
