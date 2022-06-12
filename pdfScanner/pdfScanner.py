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
    # ��������� ���� ������������ �������
    progName = os.path.basename(__file__)
    progPath = os.path.abspath(__file__).replace(progName, '')
    # ��������� ������� ���� ������������ PDF ����� (������ ���������� � ����� �������)
    pdfDocPath = progPath + 'Document-2022-05-16-192805.pdf'
    # ������� ���� ������������ txt �����
    dataTextPath = progPath + 'dataText.txt'
    return pdfDocPath, dataTextPath


def pdfToTextConv(pdfPath ,textPath):
    # �������� PDF ���������
    try:
        with fitz.open(pdfPath) as pdf: 
            # �������� txt ���������
            txtHandle = open(textPath, "wb")
            # C����� ��� �������� ���������� �� �������
            allText = []
            # ���������� ������ � �������� �� ���� ���������
            for numPage in range(len(pdf)):
                page = pdf.load_page(numPage)
                # ��� ������ ��� ����������� ����� ������� ������ (����� �������������� ����������� �� ������) 
                allText.append(page.get_text().encode("utf8"))
                txtHandle.write(allText[numPage])
    except:
        print('Oh no! PDF to txt conversion is failed.')
    
    else:
        print('Sucssesful! PDF to txt conversion completed.')





if __name__ == "__main__":
    main()