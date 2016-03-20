#coding:gb2312
from poster.encode import multipart_encode  # easy_install poster
from poster.streaminghttp import register_openers
import urllib2,urllib,simplejson,sys,hashlib,os
apikey = {'apikey': 'fa07ea9eddbc8ef8d6e6c0b433030230f7785d3aca1da3dbdb19762455a82ad7'}
url = 'https://www.virustotal.com/vtapi/v2/file/'
virustotalAPI = {'scan':url+'scan','rescan':url+'rescan','reports':url+'report'}
def scan(filepath):
    register_openers()
    file =  open(filepath, "rb")
    params = {'file': file}
    params.update(apikey)
    datagen, headers = multipart_encode(params)

    m2 = hashlib.md5()
    m2.update(file.read())
    json = report(m2.hexdigest())
    if json['response_code'] == 1:
        reportformat(json)
    else:
        request = urllib2.Request(virustotalAPI['scan'], datagen, headers)
        result = simplejson.loads(urllib2.urlopen(request).read())
        reportformat(report(result['resource']))
def report(resource ):
    parameters = {"resource":resource}
    parameters.update(apikey)
    req  = urllib2.Request(virustotalAPI['reports'], urllib.urlencode(parameters))
    str = urllib2.urlopen(req).read()
    if str == '':
        print '获取扫描结果失败,请稍后再试'
        exit(1)
    reportjson =  simplejson.loads(str)
    return reportjson
def reportformat(json):
    if json['response_code'] == 1:
        print 'scan_date\t' + json['scan_date']
        print 'scan result %d/%d'%(json['positives'],json['total'])
        for u in json['scans']:
            virus = json['scans'][u]
            print '\t{0:<20}\t{1:<40}\t{2:<10}'.format(u,virus['result'],virus['update'])
    else :
        print '请求的资源扫描未完成，请稍后再试'
def main(argv):
  scan(argv[1])

if __name__ == '__main__':
    main(sys.argv)