#coding:gb2312
import StringIO,pycurl,re,urllib
from bs4 import BeautifulSoup
import os

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
    pageurl = 'https://malwr.com/analysis/?page='
    login()

    for i in range(1,500):
        try:
            count = 0
            soup = BeautifulSoup(Curl(pageurl+'%d'%i)).select('.mono')  #先定位到子节点
            for s in soup:
                data = Curl('https://malwr.com' + s.parent['href'])
                bu = BeautifulSoup(data)
                downloadurl ='https://malwr.com'+ bu.select(".btn-primary.btn-small")[0]['href']
                date = bu.select("table.table.table-striped tbody tr td")[1].text.encode('utf-8')
                date = re.findall('\d{4}\-\d{2}',date)[0].replace('-','.') #文件上传时间

                path = os.path.join('d:\Malwar',date)
                if not os.path.exists(path):
                    os.mkdir(path)
                if downloadurl == 'https://malwr.com#':
                    continue
                count = count +1
                print '爬取第%d页第%d样本'%(i,count)
                filename = os.path.join(path,downloadurl.split('/')[-2])
                if os.path.exists(filename):
                    print downloadurl.split('/')[-2] + 'is exists'
                    continue
                open(filename,'wb').write(Curl(downloadurl,NOPROGRESS=0) )
        except pycurl.error,e:
            pass
if __name__ == '__main__':
    Test()
