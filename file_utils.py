import os
folderPath = 'output'
ext = '.txt'


def save_textfile(text: str, nameOfFile: str):
    totalFilePath = nameOfFile + ext
    print('Saving text output: ' + nameOfFile)
    try:
        os.mkdir(folderPath)
    except:
        totalFilePath = folderPath + '/' + totalFilePath

    with open(totalFilePath, 'w') as f:
        print(text, file=f)  # Python 3.x
    print('File saved!')
