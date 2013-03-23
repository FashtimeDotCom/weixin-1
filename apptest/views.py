
#encoding=utf-8
from django.http import HttpResponse
import hashlib, time, re
from xml.etree import ElementTree as ET

import WebCrawler_TiYu as wcr_ty
      
def WeixinService(request):
    
    if request.method == 'GET':
        try:
            token = 'liubing'
            args=[token,request.GET['timestamp'],request.GET['nonce']]
            args.sort()
            echostr=request.GET['echostr']
            if hashlib.sha1("".join(args)).hexdigest() == request.GET['signature']:
                return HttpResponse(echostr)
        except:
            return HttpResponse('Invalid request')
    
    if request.method == 'POST':
        try:
            reply = '''<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag></xml>'''
            if request.raw_post_data:
                received_xml=ET.fromstring(request.raw_post_data)
                content = received_xml.find('Content').text
                fromUserName = received_xml.find('ToUserName').text
                toUserName = received_xml.find('FromUserName').text
                postTime = str(int(time.time()))
                if not content:
                    return HttpResponse(reply % (toUserName,fromUserName,postTime,'please enter something'))
                if content == 'Hello2BizUser':
                    return HttpResponse(reply % (toUserName,fromUserName,postTime,'hello world!!'))
                if content == u'跑操':
                    info = '您总共跑操 %s 次' % wcr_ty.PaoCao(213110561,213110561)
                    return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                else:
                    return HttpResponse(reply % (toUserName,fromUserName,postTime,'Sorry , being developing '))
            else:
                return HttpResponse('Invalid request')
        except Exception,e:
            return HttpResponse('the site file occur errors')

    

def hello(request):
    if request.method == 'GET':
        html='hello world'
        return HttpResponse(html)
    if request.method == 'POST':
        d=request.raw_post_data
        if d:
            return HttpResponse(d)
        else:
            return HttpResponse('your post data is empty')


if __name__=="__main__":
    s='%s'%wcr_ty.PaoCao(213110561,213110561)
    print s
 
