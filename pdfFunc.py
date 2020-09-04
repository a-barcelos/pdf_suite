"""
Created on Thu Sep  3 21:23:10 2020

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
        newPath = "{}_{}_{}.pdf".format(basePath,str(s+1).zfill(3),str(e).zfill(3) )
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

def pdfStats(pdf):
    with open(pdf,"rb") as fileObj:           
        pdfReader = PyPDF2.PdfFileReader(fileObj)        
        n_pages = pdfReader.getNumPages()
        filesize = os.path.getsize(pdf)
        print('{}:\n{} páginas\n{:.4f} MB\n'.format(pdf, n_pages, filesize/1024**2) )
    return filesize, n_pages
        
    

      
   