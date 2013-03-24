
#encoding=utf-8
from django.http import HttpResponse
import hashlib, time, re
from xml.etree import ElementTree as ET

import WebCrawler_TiYu as wcr_ty
from models import UserInfo
from tools import *
import re


'''



'''




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
                # ########## 输入为空
                if not content:
                    return HttpResponse(reply % (toUserName,fromUserName,postTime,'please enter something'))
                # ######### 用户关注后，微信系统自动传输的数据
                if content == 'Hello2BizUser':
                    CheckIfUserExit(toUserName)
                    return HttpResponse(reply % (toUserName,fromUserName,postTime,'hello world!!'))
                # ########  用户更新的一卡通号和体育系密码
                if re.match(r'^ykt[\d]{9}[\n]pcpwd[\S]+$',content):
                    CheckIfUserExit(toUserName)
                    UserInfo.objects.filter(id_wx=toUserName).update(id_ykt=content[3:12],pwd_tyx=content[18:])
                    return HttpResponse(reply % (toUserName,fromUserName,postTime,'一卡通和跑操查询密码保存成功！您可以开始查询跑操了！'))
                # ########  查询跑操
                if content.replace(' ','') == u'跑操':
                    CheckIfUserExit(toUserName)

                    if not CheckIfYKTExit(toUserName):
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,'首次使用，请输入您的一卡通号和跑操查询密码，格式如下：\nykt213109999\npcpwd000000'))

                    if not CheckIfTYPwdExit(toUserName):
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,'首次使用，请输入您的跑操查询密码，格式如下：\n跑操密码000000'))

                    info = '您总共跑操 %s 次' % wcr_ty.PaoCao(GetYKT(toUserName),GetTYPwd(toUserName))
                    return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                # #######  
                
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



