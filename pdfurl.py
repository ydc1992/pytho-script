__author__ = 'Ken'
# -*- coding: utf-8 -*-
import os,re,time,urllib,urllib2

PDFList = []
url = "http://www.allitebooks.com/security/page/"

def calcRate(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    if per == 100:
        print "download complete"

for i in range(1, 3):
    request = urllib2.urlopen(url + str(i))
    data = request.read()
    PDFListTem = re.findall("<a href=\"(.*?)\" rel=\"bookmark\">", data)
    PDFList.extend(PDFListTem)
PDFSet = set(PDFList)
count = 0
for pdfurl in PDFSet:
    request = urllib2.urlopen(pdfurl)
    data = request.read()
    downurl = re.findall("href=\"(.*?)\" target=\"_blank\">Download PDF", data)
    filename = downurl[0].split('/')[-1]
    print "Start download " + filename
    local = os.path.join("D:\Ebook\\" + filename)
    urllib.urlretrieve(downurl[0], local, calcRate)