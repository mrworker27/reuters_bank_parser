import json, os, logging

from lib import getLogger

import pandas as pd

lg = getLogger(logging.INFO)

def getFinJson(dirName):
    f = open(dirName + "/finance.json", "r")
    raw = f.read()
    f.close()
    return json.loads(raw)

def getProfJson(dirName):
    f = open(dirName + "/profile.json", "r")
    raw = f.read()
    return json.loads(raw)

def getResult(mapping):
        root = os.getcwd()

        dataDir = root + "/data"

        dirList = [x[0] for x in os.walk(dataDir)]
        dirList = dirList[1:]

        result = []
        for x in dirList:
            lg.info("parsing company: %s" % x)
            jsonAll = getFinJson(x)
            if "income_annual_tables" not in jsonAll or "balance_sheet_annual_tables" not in jsonAll:
                lg.info("Does not have income and balance")
                continue

            rejected = False

            income = jsonAll["income_annual_tables"]

            incSet = set([
                "Interest Income, Bank",
                "Net Interest Income",
                "Non-Interest Income, Bank",
                "Total Interest Expense"
            ])
            incDict = {}
            for inc in income[0]["rows"]:
                if inc["name"] in incSet:
                    incDict[inc["name"]] = True
            
            for name in incSet:
                if name not in incDict:
                    lg.info("Company is not a bank by income statement")
                    rejected = True
                    break
            
            balance = jsonAll["balance_sheet_annual_tables"]

            balSet = set([
                "Cash & Due from Banks",
                "Other Earning Assets, Total",
                "Net Loans",
                "Total Assets",
                "Total Deposits",
                "Total Equity",
            ])
            
            balDict = {}

            for bal in balance[0]["rows"]:
                if bal["name"] in balSet:
                    balDict[bal["name"]] = True
            
            for name in balSet:
                if name not in balDict:
                    lg.info("Company is not a bank by balance sheet")
                    rejected = True
                    break
            
            if rejected:
                continue
            
            lg.info("Company is a bank")
            resList = {}
            for inc in income[0]["rows"]:
                if inc["name"] not in incSet:
                    continue
                for data in inc["data"]:
                    if data == "--":
                        continue
                    year = data["date"].split("-")[0]
                    if year not in resList:
                        resList[year] = {}
                    resList[year]["dir"] = x
                    resList[year]["year"] = year
                    name = ""
                    if inc["name"] in mapping:
                        name = mapping[inc["name"]]
                    else:
                        name = inc["name"]

                    resList[year][name] = float(data["value"])
                    lg.debug((name, resList[year][name]))

            for bal in balance[0]["rows"]:
                if bal["name"] not in balSet:
                    continue

                for data in bal["data"]:
                    if data == "--":
                        continue
                    
                    year = data["date"].split("-")[0]
                    if year not in resList:
                        resList[year] = {}
                    resList[year]["dir"] = x
                    resList[year]["year"] = year
                    name = ""
                    if bal["name"] in mapping:
                        name = mapping[bal["name"]]
                    else:
                        name = bal["name"]
                    resList[year][name] = float(data["value"])
                    lg.debug((name, resList[year][name]))
        
            for x in resList:
                result.append(resList[x])
                
        
        frame = pd.DataFrame()
        for r in result:
            try:
                path = r["dir"]
                profile = getProfJson(path)
                currency = profile["keystats"]["revenue"]["currency"]
                country = profile["about_info"]["country"]
                name = profile["about_info"]["company_name"] 
                r["currency"] = currency
                r["country"] = country
                r["bank_name"] = name
                r["short_name"] = r["dir"].split("/")[-1]
                del r["dir"]
                frame = frame.append(r, ignore_index = True)
                lg.info(name + " is GOOD")
            except:
                lg.warning(name + " is BAD")
        return frame
