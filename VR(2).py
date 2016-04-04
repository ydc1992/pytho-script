# coding:utf-8
  
import StringIO,pycurl,re,os
from bs4 import BeautifulSoup
import sys  
reload(sys)  
sys.setdefaultencoding('gbk')
cookie1 = '''info=xfsk_cookie_user_id_remember=jLCQLfZCocvZJpgez3Ce/WZiM2yJGCzXHChA4fkgEC7EYuxVtmt85xw3M5rOhfkJkvqgEA31KCOsrFLOkbS3fV44MDqTiNfPzmmOS+OxFknwVEuExzpnl5sB69g9lLp7KCd9ju+yoi1cA90S+xJtnDhlzoFtAYZnqJy89vodGAw=&xfsk_cookie_user_name_remember=CwpdM39jad8cW9OiPqOPw8z2C7GqUBGvRRBm1hakI/ObiFEFDvdg0WMtcBUXIdentWCXNwp1kjQzZnSWuBZfpD/5MvW7j50pbSWLsLmSMfU69Tf7Y6/StAg3zqWmARoIxTk08ELOS9RpE1snPztPLwXSa3VgCW/TtJEofa4u33I='''


cookie = '''Hm_lvt_225694c67b2c1d267db850fac9dd0170=1453869310,1454295124,1455538387;87loginname=c6bd3f84-3590-40a1-a765-a022b6f47199;CNZZDATA1255576886=1142795298-1453864149-http%253A%252F%252F87870.com%252F%7C1455537293;CNZZDATA1256099391=905726621-1453864149-http%253A%252F%252F87870.com%252F%7C1455535446;Hm_lvt_a96d250ab37bce0300949f861327c0a0=1454295634,1454323256,1455538379,1455538440; ASP.NET_SessionId=msz4j5j03iihucrmpaaulrec;Hm_lpvt_a96d250ab37bce0300949f861327c0a0=1455540079;Hm_lpvt_225694c67b2c1d267db850fac9dd0170=1455538387;info=xfsk_cookie_user_id_remember=J2DujH62IlXB/31bKIPoRgZSJBmWUmHwmPm1z4j/Uho1dZFO7M9GZpgvoNiKi0G7VROyeOcmT4EoKmhJob5hjqjmrQN1jwErvVyZJKRmc0YFipbJfM3cXSHs46Sl5Wu+G2VGK1PLMWjSe84fC7wCzGi/ylb9OralLMqe55Yz+8M=&xfsk_cookie_user_name_remember=jgWDWEK6Nybbrpb6Xoz64UX+JazOupGPU6YHEH1JsUd8IK9wTidvculLBRL7nwTzCexMSW1DtfY8P20vmveHcxss5qQ+k9r0QGF35aKVtOnXvHcYZo5BpJZSfT6aH7OEMiTX5/wBemp9sAQJcvVvIo21XnV6UOQIy70rYD6O9VE='''




# 设置curl对象 的proxy reffer cookies
def SetOpt(target_address,proxy=None,reffer=None,cookies=None):
        c = pycurl.Curl()
        c.setopt(pycurl.URL,target_address)

        if proxy != None:
            c.setopt(pycurl.PROXY,proxy)    # 设置代理
        if reffer != None:
            c.setopt(pycurl.REFERER,reffer)
        if cookies !=None:
            c.setopt(pycurl.COOKIE,cookies)
        return c


class downloader:
    def __init__(self,target_address,out_filePath,reffer,cookies,proxy=None):
        print out_filePath
        self.output_file=out_filePath       # 输出路径
        self.chunk=1*1024*1024              # 设置每次下载的块大小
        #创建存放文件的目录
        try:
            self.dir_name=self.output_file+"tmp"
            print self.dir_name
            os.mkdir(self.dir_name)
        except OSError:
            pass
                ######### 设置CURL对象 ######
        self.curl_obj= SetOpt(target_address,reffer=reffer,cookies=cookies)
        tmp_curl_obj = SetOpt(target_address,reffer=reffer,cookies=cookies)

         ##### 得到并设置下载文件的大小 ######
        tmp_curl_obj.setopt(tmp_curl_obj.NOBODY,True)
        try:
            print "Trying to get size of the file"
            tmp_curl_obj.perform()
            self.size = tmp_curl_obj.getinfo(tmp_curl_obj.CONTENT_LENGTH_DOWNLOAD)
            print  self.size
        except Exception, e:
            print e
            self.delete_temp()
            self.size = 0
        #打印进度
#        self.curl_obj.setopt(self.curl_obj.NOPROGRESS,1)
        self.curl_obj.setopt(self.curl_obj.PROGRESSFUNCTION,self.progress)

    ##### 下载 ######
    def download(self):
        if (self.size>0):
            print "Starting download. Total size: "+str(self.size)+" bytes or "+str(self.size/1024/1024)+" MB"    
        else:
            print "Starting download"

        #####  如果文件大小小于或等于块大小  就直接下载 不用分块了 #####
        if self.size <=self.chunk or self.size<0:
            self.curl_obj.fp = open(self.output_file, "wb")
            self.curl_obj.setopt(pycurl.WRITEDATA, self.curl_obj.fp)
            self.curl_obj.perform()
            self.curl_obj.fp.close()
            return
        
        #####  设置超时时间   #####
        self.curl_obj.setopt(pycurl.TIMEOUT,60*10)
        log=open("downloader.log","a")

        lim_l=0
        lim_u=self.chunk
        i=1
        ###### 下载文件  #####
        while lim_l < self.size :
            temp_output=os.path.join(self.dir_name,"output"+str(i))
            ###### 如果该分块已经存在且大小等于块大小1024*1024 说明该分块已经下载完成，继续下一次循环  #####
            if os.path.exists(temp_output) and os.path.getsize(temp_output)==self.chunk:
                #print "skip chunk ", i, lim_l
                i=i+1
                r=str(lim_l)+"-"+str(lim_u-1)  # 下载的文件分块范围 如 0-(1M-1)、 (1M-(2M-1))....
                lim_l=lim_l+self.chunk
                lim_u=lim_u+self.chunk
                continue
        
            #####  没有下载则开始下载  #####
            self.curl_obj.fp = open(temp_output, "wb")
            self.curl_obj.setopt(pycurl.WRITEDATA, self.curl_obj.fp)
            r=str(lim_l)+"-"+str(lim_u-1)
            self.curl_obj.setopt(pycurl.RANGE,r)
            
            print "download chunk", i
            ##### 下载文件   #####
            while True:
                ##### 下载完成跳出这个循环  #####
                try:
                    self.curl_obj.perform()
                    self.curl_obj.fp.close()
                    break
                ###### 异常则继续下载  #####
                except pycurl.error, e:
                    logmsg = "Pycurl error caught "+str(e)+" while downloading at download range "+str(r)+" while storing to file "+str(temp_output)+"\n"
                    log.write(logmsg)
                    print "download {} exception".format(i)
                    self.curl_obj.fp.close()
                    self.curl_obj.fp=open(temp_output,"wb")
                    continue

            i=i+1
            lim_l=lim_l+self.chunk
            lim_u=lim_u+self.chunk


    ##### 删除下载的临时文件  #####
    def delete_temp(self):
        i=1
        while True:
            temp_output=os.path.join(self.dir_name,"output"+str(i))
            if os.path.exists(temp_output):
                os.remove(temp_output)
            else:
                break
            i=i+1
        try:
            os.rmdir(self.dir_name)
        except Exception, e:
            pass
    #####  合并文件  #####
    def concatenate(self):
        ##### 合并前清空output_file的内容   #####
        fp=open(self.output_file,'wb')
        i=1

        while True:
            temp_output=os.path.join(self.dir_name,"output"+str(i))
            if not os.path.exists(temp_output):
                break
        
            ##### 读取分块内容，依次附加到output_file  #####
            print "write chunk", i
            tp=open(temp_output,"rb")
            buf = tp.read(1024 * 1024)
            fp.write(buf)
            tp.close()
            i += 1
            
        fp.close()

    #打印进度
    def progress(self,download_total,downloaded,uploaded_total,upload):
        print "To be downloaded" + str(download_total)
        print "Downloaded : " + str(downloaded)


# 获取网页数据
def GetData(url, ProxyIP=None,reffer=None):
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

# 得到页数
def GetPageCount(url):
    data = GetData(url)
    soup = BeautifulSoup(data)
    da = soup.select('.pageNav')
    page = re.findall(u"共(.*?)页", da[0].text)[0]
    return page

# 得到游戏的下载地址
def GetGameDownloadURL(pageURL):
    data = GetData(pageURL)
    soup = BeautifulSoup(data)
    try:
        da = soup.select(".download")
    except Exception,e:
        pass
    return da[0]['href']


# 得到游戏的下载页面
def GetGameDownloadPage(url):
    DownloadPageList = []
    data = GetData(url)
    soup = BeautifulSoup(data)

    da   = soup.select(".download_btn")
    for u in da:
        DownloadPageList.append('http://d.87870.com/'+u['href'])
    return DownloadPageList

def main():
    downloadPageList = []
    count = GetPageCount('http://d.87870.com/xiazai-1-0603-1_.html')

    #获取所有页的游戏下载页面
    for page in range(1,2):#int(count)):
        url = 'http://d.87870.com/xiazai-%d-0603-1_.html'% page
        downloadPageList.extend(GetGameDownloadPage(url))
    for u in downloadPageList:
        downurl = GetGameDownloadURL(u)
        data = GetData(downurl,reffer=u)
        if "store.steampowered.com" in data:
            continue
        
        GameURL = re.findall('<a href=\"(.*?)\">here',data,re.S)[0]
        
        print "downloading ", GameURL
        import urllib
        filename1 = urllib.unquote(GameURL.rpartition('/')[2])
        filename = urllib.unquote(filename1).decode('utf-8')
        print filename
        d = downloader(
            GameURL,"D:\\123\\{}".format(filename),
            reffer=u,cookies=cookie)
        d.download()
        d.concatenate()
        #d.delete_temp()

def test():
    downloadurl = "http://ptbig.putaoa.com/mancdn/up/app/10/sgqyzbltx2.0.0b_151225com.putao.PtSanguo.apk"
    out_filePath = "D:\\123\\123.apk"
    d = downloader(downloadurl,out_filePath,None,None,None)
    d.download()
    d.concatenate()
if __name__ == '__main__':
    main()
    #test()