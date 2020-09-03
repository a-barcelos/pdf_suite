# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:59:54 2020

@author: Anderson
"""

import logging, PyPDF2, os


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


merger = PyPDF2.PdfFileMerger()

#contagem de paginas do pdf segue o padra de início no 0
def splitPDF(filePath, s, e):
    basePath = filePath.replace(".pdf","")    
    with open(filePath,"rb") as fileObj:        
        pdfReader = PyPDF2.PdfFileReader(fileObj)        
        #n_pages = pdfReader.getNumPages()        
        newPath = "{}_{}_{}.pdf".format(basePath,str(s).zfill(3),str(e).zfill(3) )
        with open(newPath,"wb") as f:
            pdfWriter = PyPDF2.PdfFileWriter()
            for i in range(s,e):
                try:
                    pageObj = pdfReader.getPage(i)
                    pdfWriter.addPage(pageObj)                    
                except:
                    logger.info("Coudn't split {}".format(newPath) )
                    continue
            pdfWriter.write(f)

def promptFunc(msgList,varList):
    while True:
        try:
            for i,var in enumerate(varList):
                index = varList.index(var)
                varList[index] = int(input('{} - {}'.format(i, msgList[index]) ) )
            break
        except:
            print('Número inválido.')

def callForPDF():
    pdfs = [p for p in os.listdir() if p.endswith('pdf')]
    if len(pdfs) > 1:
        print('No diretório existem os seguintes pdfs: ')
        for i,p in enumerate(pdfs):
            print('{} - {}'.format(i+1,p) )
        while True:
            try:
                op = int(input('Qual pdf você quer dividir?\n') ) - 1
                pdf = pdfs[op]
                return pdf
                if op >= len(pdfs):
                    raise
                break
            except:
                print('Número inválido')
    elif len(pdfs) == 1:
        pdf = pdfs[0]
        return pdf
    else:
        print('Não existem pdfs no diretório.')

def pdfStats(pdf):
    with open(pdf,"rb") as fileObj:           
        pdfReader = PyPDF2.PdfFileReader(fileObj)        
        n_pages = pdfReader.getNumPages()
        filesize = os.path.getsize(pdf)
        print('{}:\n{} páginas\n{:.4f} MB\n'.format(pdf, n_pages, filesize/1024**2) )
    return filesize, n_pages
        
    

      
   