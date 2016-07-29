# -*- coding: utf-8 -*-
import sys
import os
import hashlib
import time
import os
import tornado.options
import tornado.ioloop
import tornado.web
import tornado.escape
from xml.etree import ElementTree as ET
import CollegeInfo

# 改变str编码方式为utf-8而不是默认的ascii
reload(sys)
sys.setdefaultencoding('utf8')

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "./static/"),
    "debug": True,
}

TextSetting = {
    "数据本科": CollegeInfo.getSDCSCollegeInfo,
    "数据事务": CollegeInfo.getSDCSAffairInfo,
    "政务本科": CollegeInfo.getSOGCollegeInfo,
    "政务对外": CollegeInfo.getSOGInter,
    "政务学工": CollegeInfo.getSOGStuInfo
}

class MainHandler(tornado.web.RequestHandler):
    def parse_request_xml(self,rootElem):
        msg = {}
        if rootElem.tag == 'xml':
            for child in rootElem:
                msg[child.tag] = child.text  # 获得内容
        return msg
    # 与微信服务器进行交互，确认本服务器的有效性
    def get(self):
        #获取输入参数
        signature=self.get_argument('signature')
        timestamp=self.get_argument('timestamp')
        nonce=self.get_argument('nonce')
        echostr=self.get_argument('echostr')
        #自己的token
        token="xxx"
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            self.write(echostr)

    # 信息将会post传送到这里
    def post(self):
        rawstr = self.request.body
        msg = self.parse_request_xml(ET.fromstring(rawstr))
        data = handlerResponseMsg(msg)
        self.write(data)

def handlerResponseMsg(msg):
    MsgType = tornado.escape.utf8(msg.get("MsgType"))
    Content= tornado.escape.utf8(msg.get("Content"))
    FromUserName = tornado.escape.utf8(msg.get("FromUserName"))
    CreateTime = tornado.escape.utf8(msg.get("CreateTime"))
    ToUserName = tornado.escape.utf8(msg.get("ToUserName"))
    if MsgType != "text":
        Content= "额...讲真,我只看得懂文字"
    elif not Content:
        Content= "居然发空消息！"
    elif Content in TextSetting:
        keyWord = Content
        Content = writeNotifies(TextSetting[keyWord]())
    else:
        Content = """🐽这个是菜单哦🐽
【数据院通知】
🔵数据本科：最近的本科教务通知
🔵数据事务：最近的本科事务通知
【政务院通知】
🔴政务本科：最近的本科教务通知
🔴政务对外：最近的对外交流通知
🔴政务学工：最近的学工信息
♦例如：发送'数据本科',即可得到最近数据院的本科教务通知
        """

    data = writeResponseBody(FromUserName, ToUserName, Content)
    return data

def writeResponseBody(FromUserName, ToUserName, Content):
    data = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[%s]]></MsgType>
        <Content><![CDATA[%s]]></Content>
    </xml>""" % (FromUserName,ToUserName,int(time.time()),'text',Content)
    return data

def writeNotifies(Notifies):
    Content = ""
    for notify in Notifies:
        Content = Content+"🔴"+(notify[2])+"\n"+deleteEmpty(notify[1])+"\n📅发布时间:"+deleteEmpty(notify[0])+"\n\n"
    return Content

def deleteEmpty(string):
    return ''.join(string.split())

if __name__ == "__main__":
    tornado.options.define("port", default=80, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()
    # 定义路由和事件处理函数
    application = tornado.web.Application([
        (r"/", MainHandler),
        ], **settings)
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()