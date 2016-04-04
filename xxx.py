#coding:utf-8
import pycurl,StringIO,urllib2
class blog():
    def __init__(self,pageurl,urlscope,startpage,endpage,urlreg,time,artitle):
        self.pageURL   = pageurl
        self.startPage = startpage
        self.endPage   = endpage
        self.time      = time
        self.artitle   = artitle
        self.urlscope  = urlscope
        self.urlreg    = urlreg

    def Curl(self,url, **kwargs):
        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)  # 支持https
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
        c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
        # 可扩展参数
        for k, v in kwargs.iteritems():
            c.setopt(vars(pycurl)[k], v)
        try:
            c.perform()
        except pycurl.E_SSL_CONNECT_ERROR, e:
            return
        return b.getvalue()

    def parse(self):
        for i in range(self.startPage,self.endPage):
            url = self.pageURL.replace('{0}','%d'%i)
            data = self.Curl(url)



def main():
    b = blog("http://www.freebuf.com/page/{0}",1,100)
    a = b.parse()
    c= 3

if __name__ == '__main__':
    main()
