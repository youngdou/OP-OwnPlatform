# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getCollegeInfo(url, pattern):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    try:
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reasons

    catList = response.read().decode("utf-8")

    items = re.findall(pattern, catList)
    return items

# 数据院的信息
def getSDCSCollegeInfo(option = 22):
    url = 'http://sdcs.sysu.edu.cn/?cat='+str(option)
    pattern = re.compile(r'<li>.*?<h2>.*?<span.*?fr">(.*?)</span>.*?<a href="(.*?)".*?">(.*?)</a>', re.S)

    return getCollegeInfo(url, pattern)
# getSDCSCollegeInfo()
def getSDCSAffairInfo():
    return getSDCSCollegeInfo(72)

# 政务院的信息
def getSOGCollegeInfo(option = "zh-hans/jw/bks"):
    url = "http://sog.sysu.edu.cn/"+option
    pattern = re.compile(r'<li.*?<span.*?time">(.*?)</span>.*?<a.*?"(.*?)">(.*?)</a>', re.S)
    items = getCollegeInfo(url, pattern)
    itemsList = []
    for index, item in enumerate(items):
        itemsList.append(list(item))
        itemsList[index][1] = "http://sog.sysu.edu.cn"+itemsList[index][1]

    return itemsList[0:5]
def getSOGInter():
    option = "zh-hans/zh/international_cop/fwjl"
    return getSOGCollegeInfo(option)[0:5]

def getSOGStuInfo():
    option = "zh-hans/zh/develop/xgxx"
    return getSOGCollegeInfo(option)[0:5]

# aa = getSOGCollegeInfo()
# print len(aa)
# print str(getAffairInfo())