import json
import pycurl
from html.parser import HTMLParser
from io import BytesIO 

HOST = 'https://www.reuters.com'

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.catched = dict()
        self.catchNow = (False, '')

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'id' and attr[1] == '__NEXT_DATA__':
                self.catchNow = (True, 'data_json')

    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        if self.catchNow[0]:
            self.catched[self.catchNow[1]] = data
            self.catchNow = (False, '')
    
    def release(self):
        return self.catched

def getRawHTML(url):
    b_obj = BytesIO() 
    crl = pycurl.Curl() 
    crl.setopt(crl.URL, url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform() 
    crl.close()
    get_body = b_obj.getvalue()
    return get_body.decode("utf8")

def parseCommonInfo(html):
    parser = MyHTMLParser()
    parser.feed(html)
    rawJson = parser.release()['data_json']
    parsedJson = json.loads(rawJson)
    info = parsedJson["props"]["initialState"]["markets"]["profile"]
    return info

def parseFinancialTable(html):  
    parser = MyHTMLParser()
    parser.feed(html)
    rawJson = parser.release()['data_json']
    parsedJson = json.loads(rawJson)
    tables = parsedJson["props"]["initialState"]["markets"]["financials"]["financial_tables"]
    return tables

def getData(company):
    fin = HOST + '/companies/' + company + '/financials/'
    prof = HOST + '/companies/' + company + '/profile'
    htmlProf = getRawHTML(prof)
    htmlFin = getRawHTML(fin)

    infoData = parseCommonInfo(htmlProf)
    finData = parseFinancialTable(htmlFin)

    return infoData, finData
