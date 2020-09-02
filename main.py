
from args_parser import argsParser
from pdfSplitter import splitPDF
from time import time
import os, logging, subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logger = logging.getLogger(__name__)

    

def main():  
    option = input(
                    '''
                    Escolha a opção.
                    1- juntar pdfs.
                    2- dividir pdfs.
                    '''           
                    )

    if option == '1' :
        pass  
      
    elif option == '2':
        while True:
            try:
                n = int(input('Quantas páginas cada novo arquivo deve ter?') )
                break
            except:
                print('Número ínválido.')
        pdfs = [f for f in os.listdir() if f.endswith('pdf') ]
        print('No diretório existem os seguintes PDFs:')
        for i,p in enumerate(pdfs):
            print('{} --> {}'.format(i,p) )
        
        while True:
            try:
                op = int(input('Qual pdf você quer dividir?') )
                break
            except:
                print('Número ínválido.')
        pdf = pdfs[op]
        splitPDF(pdf, n)        
    else:
        print("Opção inválida.")
        main()
        
if __name__ == '__main__':
    main()    

#logger.info("Total runtime: {}".format(time() - ts) )


