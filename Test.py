import StringIO
import os
import pycurl
import re


def GetData(url, ProxyIP=None, filePath=None):
    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
    c.setopt(pycurl.URL, url)
    if ProxyIP:
        c.setopt(pycurl.PROXY, ProxyIP)
    if filePath:
        c.fp = open(filePath, 'wb')
        c.setopt(pycurl.WRITEDATA, c.fp)
    c.perform()
    return b.getvalue()


def DownPDFFile():
    Categories = ['security']
    pdfSet = set()
    for i in range(1, 3):
        url = 'http://www.allitebooks.com/%s/page/%d/' % (Categories[0], i)
        list = re.findall("<a href=\"(.*?)\" rel=\"bookmark\">", GetData(url))
        pdfSet.update(list)
    for url in pdfSet:
        downloadurl = re.findall("href=\"(.*?)\" target=\"_blank\">Download PDF", GetData(url))
        filename = downloadurl[0].split('/')[-1]
        local = os.path.join("D:\Ebook\\" + filename)
        GetData(downloadurl[0], filePath=local)


if __name__ == '__main__':
    DownPDFFile()
