import argparse, os, logging
from time import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
ts = time()

def argsParser():
    parser = argparse.ArgumentParser(description= ''' 
    Split a file into n parts or join n parts into a file.''')
    
    #General arguments    
    parser.add_argument('-f', dest='file', metavar='File Path', type=str, 
                        help='Path to file that will be splited.')
    parser.add_argument('mode', metavar='MODE', type=str,
                        help='split or join')
    
    parser.add_argument('-e','--extension', dest='extension', metavar='Extension', type=str, 
                        help='Extension of files to join')
    
    parser.add_argument('-o','--outname', dest='outname', metavar='Filename', type=str, 
                        help='Filename to join the files under the workdir')
            
    #Chunk or n group arguments
    chorn = parser.add_mutually_exclusive_group()
    chorn.add_argument('-c', dest='chunk', metavar='Chunk Size', type=int,
                       help='Chunk size in bytes.')
    chorn.add_argument('-n', dest='nparts', metavar='n_parts', type=int,
                       help='Number of parts in which the file will be splited.')
    
    return parser.parse_args()