#coding=utf-8
from pathlib import Path
import fitz

def main():
    pdfDocPath, dataTextPath = setPath()
    pdfToTextConv(pdfDocPath, dataTextPath)
    


def setPath():
    '''
    Getting the full path to the PDF file to parse
    and to the txt file which contains the data of PDF
    Return tuple:
    :return: pdfDocPath, dataTextPath
    '''
    # Получение пути расположения проекта
    progPath = Path.home() / 'source' / 'repos' / 'pdfScanner' / 'pdfScanner'
    # Получение пути расположения PDF файла
    pdfDocPath = progPath / 'Document-2022-05-16-192805.pdf'
    # Задание пути расположения txt файла
    dataTextPath = progPath / 'dataText.txt'
    return pdfDocPath, dataTextPath


def pdfToTextConv(pdfPath ,textPath):
    # Открытие PDF документа
    try:
        with fitz.open(pdfPath) as pdf: 
            # Открытие txt документа
            txtHandle = open(textPath, "wb")
            # Cписок для хранения информации со страниц
            allText = []
            # Считывание текста с проходом по всем страницам
            for numPage in range(len(pdf)):
                page = pdf.load_page(numPage)
                # Тут каждый раз добавляется новый элемент списка (можно оптимизировать отказавшись от списка) 
                allText.append(page.get_text().encode("utf8"))
                txtHandle.write(allText[numPage])
    except:
        print('Oh no! PDF to txt conversion is failed.')
    
    else:
        print('Sucssesful! PDF to txt conversion completed.')


if __name__ == "__main__":
    main()