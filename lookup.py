import os, shutil, json
import parser

root = os.getcwd()

def logToFile(dataDir, company, idx):
    
    try:    
        infoData, finData = parser.getData(company)
    except:
        print("Parsing error")
        print("Fuckup %s #%d" % (company, idx))
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
        print("Creation of the directory %s failed" % compDir)
        print("Fuckup %s #%d" % (company, idx))
        return False
    
    print("OK %s #%d" % (company, idx))
    return True

try:
    dataDir = root + "/data"

    try:
        shutil.rmtree(dataDir)
    except OSError:
        print("Cannot delete the directory %s" % dataDir)
    
    os.mkdir(dataDir)
    companies = ['1398.HK', 'SBER.MM', 'AAPL.OQ', 'fucku']
    
    for i, company in enumerate(companies):
        logToFile(dataDir, company, i)

except OSError:
    print("Creation of the directory %s failed" % dataDir)
