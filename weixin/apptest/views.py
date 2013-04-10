
#encoding=utf-8
from django.http import HttpResponse
import hashlib, time, re
from xml.etree import ElementTree as ET

import WebCrawler_TiYu as wcr_ty
from models import UserInfo
from tools import *
import re
from WebCrawler_Lib import *

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
                fromUserName = received_xml.find('ToUserName').text
                toUserName = received_xml.find('FromUserName').text
                postTime = str(int(time.time()))
                msgtype = received_xml.find('MsgType').text
                
                # ------------------------------------------------
                #         时间消息                
                # ----------------------------------------------------
                if msgtype == u'event':
                    try:
                        event=received_xml.find('Event').text
                    except:
                        event=''
                    if not event:
                        info=u'亲！发送不能为空的！'
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    # 用户订阅  
                    if event=='subscribe':
                        info="欢迎关注小猴偷米！！\n发送 ‘跑操’   ‘今天课表’   ‘明天课表’   ‘下节课’   ‘借书信息’  等查询相应信息，\n更多查询说明请发送\n‘跑操查询说明’\n‘课表查询说明’\n‘借书查询说明’ '"
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                
                
                # ------------------------------------------------
                #          文本消息               
                #---------------------------------------------------
                if msgtype == u'text':
                    try:
                        content = received_xml.find('Content').text
                    except:
                        content=''
                    # ########## 输入为空
                    if not content:
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,'please enter something'))
                    # ######### 用户关注后，微信系统自动传输的数据
                    if content == u'Hello2BizUser': #Hello2BizUser
                        CheckIfUserExit(toUserName)
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,u'欢迎关注小猴偷米！！\n发送 ‘跑操’   ‘今天课表’   ‘明天课表’   ‘下节课’   ‘借书信息’  等查询相应信息，\n更多查询说明请发送\n‘跑操查询说明’\n‘课表查询说明’\n‘借书查询说明’ '))
                    #  #######  使用说明  ######
                    if content.replace(' ','')==u'使用说明':
                        info=u'发送 ‘跑操’   ‘今天课表’   ‘明天课表’   ‘下节课’   ‘借书信息’  等查询相应信息，\n更多查询说明请发送\n‘跑操查询说明’\n‘课表查询说明’\n‘借书查询说明’ '
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    if content.replace(' ','')==u'跑操查询说明':
                        info=u'跑操查询说明：\n跑操查询第一次使用需输入一卡通和体育系查询密码，使用方法:发送关键字\n ‘跑操’\n\n更新跑操查询绑定一卡通和密码请输入：\n一卡通213199999\n跑操密码000000\n或者:\n一卡通213199999;跑操密码000000'
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    if content.replace(' ','')==u'课表查询说明':
                        info=u'首次使用需输入一卡通,查询请发送关键词:\n‘周一课表’(周n类似)\n‘今天课表’\n‘明天课表’\n‘下节课’\n\n更改绑定一卡通请发送:\n一卡通213109999\n\n如果课表消息有误，发送‘更新课表’。'
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    if content.replace(' ','')==u'借书查询说明':
                        info=u'第一次使用需输入一卡通和图书馆查询密码\n使用方法：发送关键词:\n借书信息\n\n更新图书馆绑定一卡通和密码请发送：\n一卡通213109999\n借书密码000000\n或者:\n一卡通213109999;借书密码000000'
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    
                    
                    
                    # ########  用户更新的一卡通号和体育系密码
                    if re.match(u'^一卡通[\d]{9}[\n]跑操密码[\S]+$',content.replace(' ','')) or re.match(u'^一卡通[\d]{9};跑操密码[\S]+$',content.replace(' ','')):
                        CheckIfUserExit(toUserName)
                        UserInfo.objects.filter(id_wx=toUserName).update(id_ykt=content[3:12],pwd_tyx=content[17:])
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,u'一卡通和跑操查询密码保存成功！您可以开始查询跑操了！'))
                    # ##########  更新一卡通
                    
                    if re.match(u'^一卡通[\d]{9}$',content.replace(' ','')):
                        CheckIfUserExit(toUserName)
                        UserInfo.objects.filter(id_wx=toUserName).update(id_ykt=content[3:12])
                        UpdateKeBiao(toUserName)
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,u'一卡通保存成功！您可以开始查询了！'))
                    # #######   更新跑操密码  ###########
                    
                    if re.match(u'^跑操密码[\S]+',content.replace(' ','')):
                        CheckIfUserExit(toUserName)
                        UserInfo.objects.filter(id_wx=toUserName).update(pwd_tyx=content[4:])
                        info=u"跑操密码保存成功，您可以查询跑操了!"
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    
                    # ########   更新图书馆密码    ##########
                    if re.match(u'^借书密码[\S]+',content.replace(' ','')):
                        CheckIfUserExit(toUserName)
                        UserInfo.objects.filter(id_wx=toUserName).update(pwd_tsg=content[4:])
                        info = u"借书密码更新成功，您可以查询图书了！"
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    # ########  更新一卡通和借书密码   ###########
                    if re.match(u'^一卡通[\d]{9}\n借书密码[\S]+',content.replace(' ','')) or re.match(u'^一卡通[\d]{9};借书密码[\S]+',content.replace(' ','')):
                        CheckIfUserExit(toUserName)
                        UserInfo.objects.filter(id_wx=toUserName).update(id_ykt=content[3:12],pwd_tsg=content[17:])
                        info=u"一卡通和借书密码保存成功，您可以查询图书信息了！"
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    # ####### 更新课表    ##############
                    if re.match(u'^更新课表',content.replace(' ','')):
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u'首次使用请输入您的一卡通，格式如下：\n一卡通213109999'
                        else:
                            UpdateKeBiao(toUserName)
                            info = u'您的课表已更新成功，请输入相应关键词查询 ^_^'
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))

                    # ########  查询跑操
                    if content.replace(' ','') == u'跑操':
                        CheckIfUserExit(toUserName)

                        if not CheckIfYKTExit(toUserName):
                            return HttpResponse(reply % (toUserName,fromUserName,postTime,u'首次使用，请输入您的一卡通号和跑操查询密码，格式如下(包括汉字、换行)：\n一卡通213199999\n跑操密码000000\n或者:\n一卡通213199999;跑操密码000000'))

                        if not CheckIfTYPwdExit(toUserName):
                            return HttpResponse(reply % (toUserName,fromUserName,postTime,u'首次使用，请输入您的跑操查询密码，格式如下：\n跑操密码000000'))
                        time_paocao = wcr_ty.PaoCao(GetYKT(toUserName),GetTYPwd(toUserName))
                        if type(time_paocao) == type(False):
                            info = u'您的用户名和跑操密码貌似不对哦，请更新一卡通和跑操密码，格式如下(包括汉字、换行)：\n一卡通213199999\n跑操密码000000'
                        else:
                            info = u'您总共跑操 %s 次' %time_paocao
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    # #######  查课表   ###########
                    #  #####  按照周一到周日查询  #############
                    if content.replace(' ','') == u'周一课表':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBByDay(toUserName,1)
                            if not course:
                                info=u'亲，您周一没课'
                            else:
                                info=u"您周一的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    
                    if content.replace(' ','') == u'周二课表':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBByDay(toUserName,2)
                            if not course:
                                info=u'亲，您周二没课'
                            else:
                                info=u"您周二的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    
                    if content.replace(' ','') == u'周三课表':  # 
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBByDay(toUserName,3)
                            if not course:
                                info=u'亲，您周三没课'
                            else:
                                info=u"您周三的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    
                    if content.replace(' ','') == u'周四课表':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBByDay(toUserName,4)
                            if not course:
                                info=u'亲，您周四没课'
                            else:
                                info=u"您周四的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    
                    if content.replace(' ','') == u'周五课表':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBByDay(toUserName,5)
                            if not course:
                                info=u'亲，您周五没课'
                            else:
                                info=u"您周五的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    
                    if content.replace(' ','') == u'周六课表':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBByDay(toUserName,6)
                            if not course:
                                info=u'亲，您周六没课'
                            else:
                                info=u"您周六的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    if content.replace(' ','') == u'周日课表':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBByDay(toUserName,7)
                            if not course:
                                info=u'亲，您周日没课'
                            else:
                                info=u"您周日的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    # ########### 按照周一到周日查询完  ################
                    
                    # ########### 按照今天明天查   ############   
                    if content.replace(' ','') ==u'今天课表':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBOfToday(toUserName)
                            if not course:
                                info=u'亲，您今天没课'
                            else:
                                info=u"您今天的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                            
                        
                    if content.replace(' ','') ==u'明天课表':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course=GetKBOfTomorrow(toUserName)
                            if not course:
                                info=u'亲，您明天没课'
                            else:
                                info=u"您明天的课表是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    # #######  按照今天明天查询完   ##########
                    # ##########  按照下节课查   #############
                    if content.replace(' ','')==u'下节课':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info=u"第一次使用请输入您的一卡通号，格式如下(包括汉字):\n一卡通213109999"
                        
                        else:
                            CheckIfUserExitInKeBiao(toUserName)
                            course =GetNextCourse(toUserName)
                            if not course:
                                info=u'恭喜你，没课了！'
                            else:
                                info=u"您的下节课是:\n\n%s"%course
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))

                    # ##########   按照下节课查询完    #############
                    
                    # ###########   查询图书借阅信息   ##########
                    
                    if content.replace(' ','')==u'借书信息':
                        CheckIfUserExit(toUserName)
                        if not CheckIfYKTExit(toUserName):
                            info = u"第一次使用请输入您的一卡通号和图书馆密码，格式如下(包括汉字):\n一卡通213109999\n借书密码123456\n或者:\n一卡通213109999;借书密码123456"
                        elif not CheckIfLibPwdExit(toUserName):
                            info = u'第一次使用请输入您的图书馆密码，格式如下(包括汉字):\n借书密码000000'
                        else:
                            lib=Lib(GetYKT(toUserName),GetLibPwd(toUserName))
                            if lib.pwderror == True:
                                info=u"您的借书密码貌似不对，更新一卡通和借书密码请发送如下格式消息：\n一卡通213109999\n借书密码123456\n或者单独更新借书密码，发送消息格式：\n借书密码123456"
                            else:
                                books=lib.GetRenderList()
                                duedates=lib.GetDuedates()
                                t=u''
                                for i in range(len(books)):
                                    t+=(books[i]+u'\n')
                                    t+=(u'还书日期'+duedates[i]+u'\n\n')
                                if not t.replace(' ','').replace('\n','') :
                                    info=u"您还没有借书!"
                                else:
                                    info=u"您的借书信息如下：\n%s"%t
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))  
                    # ############  查询图书借阅信息完  #################
                    if content.replace(' ','')==u'当前时间':
                        info=GetCurrentTime()
                        return HttpResponse(reply % (toUserName,fromUserName,postTime,info))
                    
                    else:
                        info=u'发送 ‘跑操’   ‘今天课表’   ‘明天课表’   ‘下节课’   ‘借书信息’  等查询相应信息，\n更多查询说明请发送\n‘跑操查询说明’\n‘课表查询说明’\n‘借书查询说明’ '
                        return HttpResponse(reply%(toUserName,fromUserName,postTime,info) )
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



