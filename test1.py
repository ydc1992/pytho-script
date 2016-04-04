import StringIO,pycurl

def Curl(url):
    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.SSL_VERIFYPEER,0)
    c.setopt(pycurl.SSL_VERIFYHOST,0)
    c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
    c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
    return b.getvalue()