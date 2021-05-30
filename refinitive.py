import urllib.parse
import json
import pycurl
import logging
from html.parser import HTMLParser
from io import BytesIO 
from lib import getLogger

HOST = 'https://api-eit.refinitiv.com/permid'

lg = getLogger(logging.DEBUG)

def getRefinResp(url):
    lg.debug("Requesting PERMID ... %s" % url)
    b_obj = BytesIO() 
    crl = pycurl.Curl() 
    crl.setopt(crl.URL, url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform() 
    crl.close()
    get_body = b_obj.getvalue()
    lg.debug("Done")
    return get_body.decode("utf8")

def extractTicker(raw):
    parsed = json.loads(raw)
    quotes = parsed["result"]["organizations"]["entities"]
    num = parsed["result"]["organizations"]["num"]
    RIClist = []
    for q in quotes:
        if "primaryTicker" in q:
            RIClist.append(q)
    return RIClist, num

def extractRIC(raw):
    parsed = json.loads(raw)
    quotes = parsed["result"]["quotes"]["entities"]
    num = parsed["result"]["quotes"]["num"]
    RIClist = []
    for q in quotes:
        if "hasRIC" in q and '^' not in q["hasRIC"]:
            RIClist.append(q)

    return RIClist, num

def constructRequest(query, start, number, token):
    x = urllib
    q = urllib.parse.urlencode({"q": query, "access-token" : token, "start" : start, "num" : number})
    url = HOST + "/search?" + q
    return url

def getStuff(query, number, times, token, f):
    idx = 1
    totalList = []
    lg.info("Processing batch size = %d [%d times]" % (number, times))
    realNumber = 0
    for i in range(times):
        try:
            url = constructRequest(query, idx, number, token)
            resp = getRefinResp(url)
            curList, cnt = f(resp)
            realNumber += cnt
            if cnt == 0:
                break
            totalList += curList
        except:
            lg.warning("FAIL")
        idx += number

    lg.info("TOTAL: %d responses" % len(totalList))
    return totalList

print("Enter PERMID token:")
token = input()
print("Enter mode (0: names -> tickers) (1: tickers -> rics)")
mode = int(input())

if mode == 0:
    f = open("names.json", "r")
    inp = f.read()
    f.close()

    names = json.loads(inp)
    print(len(names))
    res = []
    for name in names: 
        print(name)
        r = getStuff(name, 10, 1, token, extractTicker)
        res += r

    lst = set()
    for r in res:
        lst.add(r["primaryTicker"])

    lg.info("TOTAL: %d tickers" % len(lst))

    f = open("tickers.json", "w")
    f.write(json.dumps(list(lst)))
    f.close()
else:
    f = open("tickers.json", "r")
    inp = f.read()
    f.close()

    tickers = json.loads(inp)
    
    # tickers = tickers[0:10]
    
    res = []
    for t in tickers:
        print(t)
        r = getStuff(t, 2, 1, token, extractRIC)
        res += r

    lst = set()
    for r in res:
        lst.add(r["hasRIC"])
    lg.info("TOTAL: %d RICs" % len(lst))

    f = open("rics.json", "w")
    f.write(json.dumps(list(lst)))
    f.close()
