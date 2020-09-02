# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:59:54 2020

@author: Anderson
"""

import logging, PyPDF2


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#contagem de paginas do pdf segue o padra de início no 0
def splitPDF(filePath, s, e):
    basePath = filePath.replace(".pdf","")    
    with open(filePath,"rb") as fileObj:        
        pdfReader = PyPDF2.PdfFileReader(fileObj)        
        #n_pages = pdfReader.getNumPages()        
        for i in range(s,e):
            try:
                pageObj = pdfReader.getPage(i)
                newPath = "{}_{}_{}.pdf".format(basePath,str(s).zfill(3),str(e).zfill(3) )
                with open(newPath,"wb") as f:
                    pdfWriter = PyPDF2.PdfFileWriter()
                    pdfWriter.addPage(pageObj)
                    pdfWriter.write(f)
            except:
                logger.info("Coudn't split {}".format(newPath) )
                continue



      
   