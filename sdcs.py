# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

url = 'http://sdcs.sysu.edu.cn/?cat=22'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    # pageCode = response.read()
    # print pageCode
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reasons

catList = response.read().decode("utf-8")
# pattern = re.compile(r"<div.*?cat_list.*?", re.S)
pattern = re.compile(r'<li>.*?<h2>.*?<span.*?fr">(.*?)</span>.*?<a href="(.*?)".*?">(.*?)</a>', re.S)

items = re.findall(pattern, catList)
for item in items:
	for i in item:
		print i