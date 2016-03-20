#coding:gb2312

import StringIO,pycurl
from bs4 import BeautifulSoup

def GetData(url, ProxyIP=None,reffer=None,cookie = None):
    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.COOKIE,cookie)
    if reffer:
        c.setopt(pycurl.REFERER,reffer)
    c.perform()
    return b.getvalue()

def main():
    url = 'http://www.ishadowsocks.com/'
    data = GetData(url)
    soup = BeautifulSoup(data)
    da = soup.select('section#free div.container div.row div.col-lg-4.text-center')
    data = da[1].text

    for u in data:
        f = open()

if __name__ == '__main__':
    main()