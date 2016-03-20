#coding:utf-8
import StringIO,pycurl,re,time


def Curl(url,**kwargs):
    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.SSL_VERIFYPEER,0)  #支持https
    c.setopt(pycurl.SSL_VERIFYHOST,0)
    c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
    c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
    c.setopt(pycurl.NOPROGRESS,0)   # 显示下载进度
    #可扩展参数
    for k, v in kwargs.iteritems():
        c.setopt(vars(pycurl)[k], v)
    try:
        c.perform()
    except pycurl.E_SSL_CONNECT_ERROR,e:
        return
    return b.getvalue()

def main():
    url = 'http://malc0de.com/database/'
    da = Curl(url)
    print da
    time.sleep(5)
    da = Curl(url)
    print da

if __name__ == '__main__':
    main()