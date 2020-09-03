

from pdfFunc import splitPDF, pdfStats, callForPDF, merger
import logging, os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logger = logging.getLogger(__name__)
        
def main():
    option = input('''
    Escolha a opção: 
    1- juntar pdfs.
    2- dividir pdf.\n''')

    if option == '1' :
        pdfs = sorted([p for p in os.listdir() if p.endswith('pdf') ] )
        if len(pdfs) > 1:            
            filename = input('Qual o nome do novo arquivo pdf?\n')
            for p in pdfs:
                merger.append(p)
            merger.write('{}.pdf'.format(filename) )
            print('PDFs unidos no arquivo {}.pdf'.format(filename) )
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
                    n = int(input('Em quantas partes você quer dividir?\n'))
                    if n >= n_pages:
                        print('Número de partes maior do que o número de páginas. Nada a fazer.\n')
                    else:                        
                        if n_pages % n != 0:                            
                            nPags = n_pages//n                            
                            s = 0
                            e = nPags
                            for i in range(0, (n-1)*nPags, nPags):
                                splitPDF(pdf, s, e)
                                s = e
                                e = e + nPags
                            e = n_pages
                            splitPDF(pdf, s, e)                              
                        else:                            
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


