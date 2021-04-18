import pycurl
from html.parser import HTMLParser
from io import BytesIO 

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag, attrs)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

def getRawHTML(url):
    b_obj = BytesIO() 
    crl = pycurl.Curl() 
    crl.setopt(crl.URL, url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform() 
    crl.close()
    get_body = b_obj.getvalue()
    return get_body.decode("utf8")

html = getRawHTML('https://wiki.python.org/moin/BeginnersGuide')
parser = MyHTMLParser()
parser.feed(html)
