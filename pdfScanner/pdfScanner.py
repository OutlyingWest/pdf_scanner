#coding=utf-8
#from pathlib import Path
import os
import fitz

def main():
    pdfDocPath, dataTextPath = getPath()
    pdfToTextConv(pdfDocPath, dataTextPath)
    


def getPath():
    '''
    Getting the full path to the PDF file to parse
    and to the txt file which contains the data of PDF
    Return tuple:
    :return: pdfDocPath, dataTextPath
    '''
    # Получение пути расположения проекта
    progName = os.path.basename(__file__)
    progPath = os.path.abspath(__file__).replace(progName, '')
    # Получение полного пути расположения PDF файла (должен находиться в папке проекта)
    pdfDocPath = progPath + 'Document-2022-05-16-192805.pdf'
    # Задание пути расположения txt файла
    dataTextPath = progPath + 'dataText.txt'
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