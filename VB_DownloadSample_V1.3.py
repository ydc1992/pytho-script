#coding:gb2312
import optparse,sys,os,urllib,urllib2,time

API_KEY = 'c2d3e2f082b144a6af9b710a685ae5723371cad56bd44a6cbb9ff66cca374293' #替换成自己的API_KEY
BASE_URL = "http://sample.virusbook.cn:18081/api/v1/file/"

def Clip():
    pass

def downloadSample(hash,path,vc):
    filePath = os.path.join(path, hash)
    url = BASE_URL + "not_detected_sample"
    parameters = {
        "sha256": hash,
        "vc": vc,
        "apikey": API_KEY
    }
    data = urllib.urlencode(parameters)
    tryCount = 10

    while tryCount > 0:
        try:
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)

            if response.code != 200:
                tryCount -= 1
                time.sleep(5)
                print "downloadSample retry..."
                continue
            else:
                # get the file content.
                content = response.read()

                fo = open(filePath, 'wb')
                fo.write(content)
                fo.close()

            break
        except Exception, e:
            tryCount -= 1
            if tryCount > 0:
                print 'get connection exception, retrying ...'
                time.sleep(3)
            else:
                print 'get connection exception, do not retry, exit.'
                raise e

def main():
    parser = optparse.OptionParser(usage = """
    %prog -c -f <out_filepath>
    -c Get hash form clipboard
    -f Sample save path
    """)

    parser.add_option("-c",action="store_true", dest = "clip", default = None)
    parser.add_option("-f",dest="outfile",default=None)
    # 获取命令行参数
    (options, arguments) = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_usage()
        return -1
    path = options.outfile


if __name__ == '__main__':
    main()