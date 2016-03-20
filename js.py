#coding:gb2312
from selenium import webdriver
from bs4 import BeautifulSoup
import time,pycurl,StringIO

url = 'https://www.hybrid-analysis.com/recent-submissions?filter=file'

driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs\bin\phantomjs.exe')
driver.get(url)
time.sleep(7)
page_source =  driver.page_source
#data = driver.find_element_by_id('submissions')
driver.get(url)
page_source = driver.page_source
print page_source.encode('utf-8')