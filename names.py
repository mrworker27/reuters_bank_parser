import json
import pycurl
from html.parser import HTMLParser
from io import BytesIO 

HOST = 'https://www.reuters.com'

url = 'https://www.globalbrandsmagazine.com/list-of-banks-by-country/'

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.catched = {"list": []}
        self.catchNow = (False, '')

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.catchNow = (True, "list")
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        if self.catchNow[0]:
            self.catched[self.catchNow[1]].append(data)

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

parser = MyHTMLParser()
html = getRawHTML(url)
parser.feed(html)
raw = parser.release()["list"]
clean = []
for x in raw:
    if '\n' not in x and '\t' not in x:
        sp = x.split('(')[0]
        clean.append(sp)

js = json.dumps(clean[:-65])

f = open("names.json", "w")
f.write(js)
f.close()
