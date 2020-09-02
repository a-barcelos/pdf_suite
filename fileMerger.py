# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#! python3

from time import time
import os, logging, subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logger = logging.getLogger(__name__)

    
def main():
    option = input(
'''
Extensão dos arquivos a juntar?
1- pdf
2- txt
'''                 )
    
    extDict = {'1': '.pdf', '2': '.txt'
               }
    if option in extDict:
        outname = input("Nome do novo arquivo:")
        ts = time()
        invChar = '/\*<>?:'
        for c in invChar:
            outname = outname.replace(c,'')
        currDir = os.getcwd()
        outname_full = outname + extDict[option]
        subprocess.Popen(["powershell.exe", "{}\\fileSplitter.exe join -e {} -o {}".format(currDir, extDict[option],outname_full)])
        logger.info("Total runtime: {}".format(time() - ts) )
    else:
        print("Opção inválida.")
        main()
if __name__ == '__main__':
    main()    


    

