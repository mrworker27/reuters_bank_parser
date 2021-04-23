import os, shutil, json, logging
import parser
from lib import getLogger

lg = getLogger(logging.INFO)

root = os.getcwd()

def logToFile(dataDir, company, idx):
    
    try:    
        infoData, finData = parser.getData(company)
    except:
        lg.warning("Parsing error")
        lg.warning("Fuckup %s #%d" % (company, idx))
        return False
    
    try:
        compDir = dataDir + "/" + company
        os.mkdir(compDir)
        
        f = open(compDir + "/profile.json", "w")
        f.write(json.dumps(infoData))
        f.close()
        
        f = open(compDir + "/finance.json", "w")
        f.write(json.dumps(finData))
        f.close()

    except OSError:
        lg.warning("Creation of the directory %s failed" % compDir)
        lg.warning("Fuckup %s #%d" % (company, idx))
        return False
    
    lg.info("PARSED OK %s #%d" % (company, idx))
    return True

def saveFiles(companies):
    lg.info("Parsing companies to files")
    try:
        dataDir = root + "/data"

        try:
            shutil.rmtree(dataDir)
        except OSError:
            lg.warning("Cannot delete the directory %s" % dataDir)
        
        os.mkdir(dataDir)
        companies = ['1398.HK', 'SBER.MM', 'AAPL.OQ', 'fucku']
        
        for i, company in enumerate(companies):
            logToFile(dataDir, company, i)

    except OSError:
        lg.warning("Creation of the directory %s failed" % dataDir)
