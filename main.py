"""
Created on Thu Sep  3 21:23:10 2020

@author: Anderson
"""

from optionsFunc import option1, option2, option3
import logging, os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logger = logging.getLogger(__name__)
        
def main():        
    option = int(input('''Escolha a opção:\n1 - Juntar pdfs\n2 - Dividir pdf\n3 - Extrair Páginas\n''') )
    pdfs = sorted([p.lower() for p in os.listdir() if p.endswith('pdf') ] )
    if option == 1:
        option1(pdfs)
    elif option == 2:
        option2(pdfs)
    elif option == 3:
        option3(pdfs)
    else:
        print('Opção inválida')   
        
if __name__ == '__main__':
    main()    

#logger.info("Total runtime: {}".format(time() - ts) )


