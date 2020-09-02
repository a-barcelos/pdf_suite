
from args_parser import argsParser
from pdfSplitter import splitPDF
from time import time
import os, logging, subprocess, PyPDF2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logger = logging.getLogger(__name__)

    
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
    
        
def main():
    option = input('''
    Escolha a opção: 
    1- juntar pdfs.
    2- dividir pdf.\n''')

    if option == '1' :
        pass  
      
    elif option == '2':
        while True:
            try:
                mode = int(input('''
                Dividir o pdf em: 
                1 - n partes.
                2 - Da pagina x à página y.\n''' ) )
                
                pdf = callForPDF()
                filesize, n_pages = pdfStats(pdf)

                if mode == 1:
                    n = int(input('Em quantas partes você quer dividir?'))
                    if n >= n_pages:
                        print('Número de partes maior do que o número de páginas. Nada a fazer.')
                    else:                        
                        if n_pages % n != 0:
                            n_ranges = n + 1
                            nPags = n_pages//n
                            remainder = n_pages % n
                            s = 0
                            e = nPags
                            for i in range(0, n_pages, nPags):
                                splitPDF(pdf, s, e)
                                s = e
                                e = e + nPags
                            e = e - nPags + remainder
                            splitPDF(pdf, s, e)                              
                        else:
                            n_ranges = n
                            nPags = n_pages//n
                            s = 0
                            e = nPags
                            for i in range(0, n_pages, nPags):
                                splitPDF(pdf, s, e)
                                s = e
                                e = e + nPags          
                        
                elif mode == 2:
                    start = int(input('Qual a página inicial? (a 1ª página é a de número 0)\n'))
                    end = int(input('Qual a página final?\n'))
                    splitPDF(pdf, start, end)
                else:
                    print('Opção inválida.')
                    raise
                break
            except:
                print('Opção inválida.')
        
    else:
        print("Opção inválida.")
        main()
        
if __name__ == '__main__':
    main()    

#logger.info("Total runtime: {}".format(time() - ts) )


