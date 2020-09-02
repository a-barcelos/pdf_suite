# -*- coding: utf-8 -*-
import base64, re, os, requests, PyPDF2, logging
from time import sleep
from bs4 import BeautifulSoup
from tika import parser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dateSelUrl = "http://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_data.php"
baseUrl = "http://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_edicao.php?data="
ptsBaseUrl = "http://www.ioerj.com.br/portal/modules/conteudoonline/"
sessionBaseUrl = "http://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session="
pdfBaseUrl = "http://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?k="

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def write_list2txt(list_var, filename):
    with open(filename,"w", encoding="utf-8") as f:
        for i,l in enumerate(list_var):
            if i < len(list_var)-1:
                f.write("{}\n".format(l))
            else:
                f.write("{}".format(l))

def read_txt2list(filename):
    with open(filename, encoding="utf-8") as f:
        list_var = f.read().split("\n")
    return list_var

def encode_n(ds,n=1):
    if n > 0:
        temp = base64.b64encode(ds.encode()).decode()
        return encode_n(temp, n-1)
    else:
        return ds       
    
def decode_n(es, n=3):    
    if n > 0:
        temp = base64.b64decode(es).decode()
        return decode_n(temp, n-1)        
    else:
        return es

def baseStr(ds):
    a = ds[:12]
    b = ds[12:]
    c = a + 'P' + b
    return c[:-10]

def getSessionStr(href):
    regex = re.compile(r'(http://www\.ioerj\.com\.br/portal/modules/conteudoonline/mostra_edicao\.php\?session=)(.*)')
    mo = regex.search(href)
    return mo.group(2)

def map2pgUrl(sessionUrl):
    sessionStr = getSessionStr(sessionUrl)
    ds = decode_n(sessionStr)
    bStr = baseStr(ds)
    return pdfBaseUrl+bStr

def t_driver(headless=True):   
    options = webdriver.FirefoxOptions()
    options.headless = headless
    driver = webdriver.Firefox(options=options)
    return driver

#todo: catch timeout error and other specific errors
def get_partes(driver, date):
    global baseUrl, sessionBaseUrl, pdfBaseUrl
    editionUrl = baseUrl + encode_n(date)    
    try:
        driver.get(editionUrl)
        partes = WebDriverWait(driver,3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'a[href*="mostra_edicao.php?"]') )
                                              )
    except:
        with open('zeroPartes.txt','a') as f:
            f.write(date+'\n')
        print("{} edition has no Partes".format(date) )
        return None
    partesList = []    
    for p in partes:
        name = date + "_" + p.text.replace(' ','').replace('(','_').replace('-','').replace(')','')
        href = p.get_attribute('href')
        sessionStr = getSessionStr(href)
        decodedStr = decode_n(sessionStr)
        pdfBaseStr = baseStr(decodedStr)
        sessionUrl = sessionBaseUrl + sessionStr
        # pageBaseUrl + pageNumber = pdfUrl 
        pageBaseUrl = pdfBaseUrl + pdfBaseStr
        partesList.append((sessionUrl, pageBaseUrl, name))
    return partesList

#todo: catch timeout error and other specific errors
def get_npages(driver, sessionUrl):        
    driver.get(sessionUrl)
    pgs = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@data-page-number]') ) )
    return len(pgs)

def createPreQueueList(drv, date):    
    preQueueList = []    
    partesList = get_partes(drv, date)
    for p in partesList: #if partesList is None, this will throw an exception here
        try:
            sessionUrl = p[0]
            pgBaseUrl = p[1]
            name = p[2].lower()
            npages = get_npages(drv, sessionUrl)
            preQueueList.append((pgBaseUrl, name, str(npages) ) )
        except:            
            with open('partesError.txt','a') as f:
                f.write("{},{},{}\n".format(sessionUrl, name, date) )
            continue            
    return preQueueList

def get_editionLinks(dump=True): 
    global dateSelUrl, baseUrl
    res = requests.get(dateSelUrl)
    soup = BeautifulSoup(res.content,features="lxml")
    datesTags = soup.find_all(href=re.compile("do_seleciona_edicao.php") )
    if dump:
        with open("editionLinks.txt", "w") as f:        
            for tag in datesTags:
                encDate = tag.attrs['href'].replace("do_seleciona_edicao.php?data=","")
                date = decode_n(encDate,1)
                if tag != datesTags[-1]:
                    f.write("{}{},{}\n".format(baseUrl,encDate,date))
                else:
                    f.write("{}{},{}".format(baseUrl,encDate,date))
    else:
        editionLinksList = []
        for tag in datesTags:
            encDate = tag.attrs['href'].replace("do_seleciona_edicao.php?data=","")
            date = decode_n(encDate,1)
            editionLinksList.append("{}{},{}".format(baseUrl,encDate,date) )
        return editionLinksList

def request_partes(edUrl, date):
    global ptsBaseUrl
    res = requests.get(edUrl)
    soup = BeautifulSoup(res.content, features="lxml")
    partesTags = soup.find_all(href=re.compile("mostra_edicao.php") )
    ptsURLsList = []
    for p in partesTags:
        name =  p.text.lower().replace(" ","_").replace("(","").replace(")","")
        ptsURLsList.append(ptsBaseUrl+p.attrs['href']+","+date+","+name)       
    return ptsURLsList
    
def scrape(driver, link, path):
    driver.get(link)
    iframe = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.TAG_NAME,"iframe") ) )
    driver.switch_to.frame(iframe)
    text =''
    textEls = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="textLayer"]/*')))
    text += '\n'.join([t.text for t in textEls])
    with open(path,'w',encoding="UTF-8") as f:
        f.write(text)

def pdf2txt(pdf):    
    raw = parser.from_file(pdf)
    txt = raw['content']
    return txt.strip()

def splitPDF(filePath):
    basePath = filePath.replace(".pdf","")    
    with open(filePath,"rb") as fileObj:        
        pdfReader = PyPDF2.PdfFileReader(fileObj)        
        n_pages = pdfReader.getNumPages()
        for n in range(n_pages):
            try:
                pageObj = pdfReader.getPage(n)
                if n < 10:
                    pagePath = "{}_0{}.pdf".format(basePath,n)
                else:
                    pagePath = "{}_{}.pdf".format(basePath,n)
                with open(pagePath,"wb") as f:
                    pdfWriter = PyPDF2.PdfFileWriter()
                    pdfWriter.addPage(pageObj)
                    pdfWriter.write(f)
            except:
                logger.info("Coudn't split {}".format(pagePath) )
                continue
    

def write_txt(text, file_path):
    with open(file_path,"w", encoding="utf-8") as f:
        f.write(text)        


    



