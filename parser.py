import json
import pycurl
from html.parser import HTMLParser
from io import BytesIO 

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
    return parsedJson

def parseFinancialTable(html):  
    parser = MyHTMLParser()
    parser.feed(html)
    rawJson = parser.release()['data_json']
    parsedJson = json.loads(rawJson)
    tables = parsedJson["props"]["initialState"]["markets"]["financials"]["financial_tables"]
    return tables

host = 'https://www.reuters.com'
company = '1398.HK'

fin = host + '/companies/' + company + '/financials/'
prof = host + '/companies/' + company + '/profile'

html = getRawHTML(prof)
print(parseCommonInfo(html))
#print(parseFinancialTable(html))
