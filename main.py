
from args_parser import argsParser
from pdfSplitter import splitPDF
from time import time
import os, logging, subprocess

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
            print('{} - {}'.format(i,p) )
        while True:
            try:
                op = int(input('Qual pdf você quer dividir?') )
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
        
def main():
    option = input('''Escolha a opção: 
                   1- juntar pdfs.
                   2- dividir pdf.'''
                    )

    if option == '1' :
        pass  
      
    elif option == '2':
        while True:
            try:
                mode = int(input('''Dividir o pdf em: 
                               1 - n partes.
                               2 - Da pagina x à página y.'''))
                
                pdf = callForPDF()

                if mode == 1:
                    n = int(input('Em quantas partes você quer dividir?'))
                else:
                    start = int(input('Qual a página inicial? \(a 1ª página é a de número 0\)'))
                    end = int(input('Qual a página final?'))
                    splitPDF(pdf, start, end)   2                          
                break
            except:
                print('Número ínválido.')
        
    else:
        print("Opção inválida.")
        main()
        
if __name__ == '__main__':
    main()    

#logger.info("Total runtime: {}".format(time() - ts) )


