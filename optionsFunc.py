"""
Created on Thu Sep  3 21:23:10 2020

@author: Anderson
"""

from pdfFunc import splitPDF, pdfStats, merger
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logger = logging.getLogger(__name__)
        

def option1(pdfs):
    if len(pdfs) <= 1:
        print('\nDeve haver pelo menos 2 PDFs no diretório. Nada a fazer.')
    else:        
        filename = input('\nQual o nome do novo arquivo pdf?\n')
        for p in pdfs:
            merger.append(p)
        merger.write('{}.pdf'.format(filename) )
        print('\nNovo PDF: {}.pdf'.format(filename) )

def option2(pdfs):
    if len(pdfs) < 1:
        print('\nNão há PDFs no diretório. Nada a fazer.')
    else:
        print('\nPDF(s) no diretório:')
        for i,p in enumerate(pdfs):
            print('{} - {}'.format(i+1, p) )
        pdf = pdfs[int(input('\nDividir qual PDF?\n')) - 1]
        filesize, n_pages = pdfStats(pdf)
        #tratar exceção de números impossíveis de se dividir
        n = int(input('\nDividir em quantas partes?\n') )
        if n >= n_pages or n < 1:
            print('\nO número de partes deve estar entre 2 e o número de páginas. Nada a fazer.\n')
        elif n_pages % n != 0:
            nPags = n_pages//n
            s = 0
            e = nPags
            for i in range(0, (n-1)*nPags, nPags):
                print('Novo arquivo: {}'.format(splitPDF(pdf, s, e) ) )
                s = e
                e = e + nPags
            e = n_pages
            print('Novo arquivo: {}'.format(splitPDF(pdf, s, e) ) )
        else:                            
            nPags = n_pages//n
            s = 0
            e = nPags
            for i in range(0, n_pages, nPags):
                print('Novo arquivo: {}'.format(splitPDF(pdf, s, e) ) )
                s = e
                e = e + nPags

def option3(pdfs):
    if len(pdfs) < 1:
        print('\nNão há PDFs no diretório. Nada a fazer.')
    else:
        print('\nPDF(s) no diretório:')
        for i,p in enumerate(pdfs):
            print('{} - {}'.format(i+1, p) )        
        pdf = pdfs[int(input('\nExtrair de qual PDF?\n')) - 1]        
        filesize, n_pages = pdfStats(pdf)
    start = int(input('\nQual a página inicial?\n')) - 1
    end = int(input('\nQual a página final?\n') )
    print('Novo arquivo: {}'.format(splitPDF(pdf, start, end) ) )
        
def exit_func():
    op = input('Sair do programa? (S/N)')
    if op.lower() == 's':
        return True
    elif op.lower() == 'n':
        return False
    else:
        print('Opção inválida.')
        exit_func()


