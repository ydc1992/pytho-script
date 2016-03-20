#coding:gb2312
import StringIO,pycurl,re,urllib
from bs4 import BeautifulSoup

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
    #可扩展参数
    for k, v in kwargs.iteritems():
        c.setopt(vars(pycurl)[k], v)
    try:
        c.perform()
    except pycurl.E_SSL_CONNECT_ERROR,e:
        return
    return b.getvalue()
# 模拟登陆
def login():
    loginurl = 'https://malwr.com/account/login/'
    crsftoken = re.findall('name=\'csrfmiddlewaretoken\' value=\'(.*?)\'\s*/>',
                           Curl(loginurl))[0]
    post = urllib.urlencode({
        'csrfmiddlewaretoken': crsftoken,
        'username':'ken_yang',
        'password':'sw3ptk',
        'next':''
        })
    Curl(loginurl,POSTFIELDS=post)

def Test():
    BeautifulSoup('lxml')
    pageurl = 'https://malwr.com/analysis/?page='
    login()
    count = 0
    for i in range(1,500):
        try:
            soup = BeautifulSoup(Curl(pageurl+'%d'%i)).select('.mono')  #先定位到子节点
            for s in soup:
                data = Curl('https://malwr.com' + s.parent['href'])
                downloadurl ='https://malwr.com'+ BeautifulSoup(data).select(".btn-primary.btn-small")[0]['href']
                if downloadurl == 'https://malwr.com#':  # 文件没有被分享时的下载网址，跳过这一次循环直接下一次循环
                    continue
                count = count +1
                print '爬取第%d页第%d样本'%(i,count)
                open('D:\\Malwar\\' + downloadurl.split('/')[-2],'wb').write(Curl(downloadurl,NOPROGRESS=0) )
        except pycurl.E_SSL_CONNECT_ERROR,e:
            pass

if __name__ == '__main__':
    Test()
