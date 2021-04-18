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

def extractRIC(raw):
    parsed = json.loads(raw)
    quotes = parsed["result"]["quotes"]["entities"]
    RIClist = []
    for q in quotes:
        if "hasRIC" in q:
            RIClist.append(q)
    return RIClist

def filterRIC(lst):
    filtered = []
    quoteSet = set()
    for q in lst:
        if '^' not in q["hasRIC"] and "isQuoteOf" in q:
            if q["isQuoteOf"] not in quoteSet:
                filtered.append(q)
                quoteSet.add(q["isQuoteOf"])
    return filtered

def constructRequest(query, start, number, token):
    url = HOST + "/search?q=%s&access-token=%s&start=%d&num=%d" % (query, token, start, number)
    return url

def getRICs(query, number, times, token):
    idx = 1
    totalList = []
    lg.info("Processing batch size = %d [%d times]" % (number, times))
    for i in range(times):
        try:
            url = constructRequest(query, idx, number, token)
            resp = getRefinResp(url)
            curList = extractRIC(resp)
            totalList += curList
        except:
            lg.warning("FAIL")
        idx += number
    return filterRIC(totalList)

print("Enter PERMID token:")
token = input()
res = getRICs("bank", 200, 20, token)

lst = []
for r in res:
    lst.append(r["hasRIC"])

lg.info("TOTAL: %d tickers" % len(lst))

f = open("rics.json", "w")
f.write(json.dumps(lst))
f.close()
