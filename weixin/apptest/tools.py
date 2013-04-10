
#encoding:utf-8


from models import UserInfo,KB
from WebCrawler_KeBiao import KeBiao

import datetime,time
import re

from schoolinfo import NewTermDate


def CheckIfUserExit(username):
    usr_list=UserInfo.objects.all()
    wx_id_list=[]
    for item in usr_list:
        wx_id_list.append(item.id_wx)

    if username not in wx_id_list:
        UserInfo.objects.create(id_wx=username)

def CheckIfYKTExit(usrname):
    usr=UserInfo.objects.filter(id_wx = usrname)
    if type(usr[0].id_ykt)==type(u'www'):
        return True
    else:
        return False



def CheckIfTYPwdExit(usrname):
    usr=UserInfo.objects.filter(id_wx = usrname)
    if type(usr[0].pwd_tyx)==type(u'www'):
        return True
    else:
        return False
    
def CheckIfLibPwdExit(usrname):
    usr=UserInfo.objects.filter(id_wx = usrname)
    if type(usr[0].pwd_tsg)==type(u'www'):
        return True
    else:
        return False
    
'''    
def CheckIfLibPwdExit(usrname):
    usr=UserInfo.objects.filter(id_wx = usrname)
    if type(usr[0].pwd_tsg)==type(u'www'):
        return True
    else:
        return False
'''
    
def CheckIfXHExit():
    usr=UserInfo.objects.filter(id_wx = usrname)
    if type(usr[0].id_xh)==type(u'www'):
        return True
    else:
        return False
        
    

def GetYKT(usrname):
    usr=UserInfo.objects.filter(id_wx = usrname)
    return usr[0].id_ykt

def GetTYPwd(usrname):
    usr=UserInfo.objects.filter(id_wx = usrname)
    return usr[0].pwd_tyx

def GetLibPwd(usrname):
    usr=UserInfo.objects.filter(id_wx=usrname)
    return usr[0].pwd_tsg


def GetSingualKB(usrname,t):
    usr = KB.objects.filter(id_wx = usrname)
    
    def tmpfun(x):
        return x
    
    course={
    1:lambda:tmpfun(usr[0].course_1),
    2:lambda:tmpfun(usr[0].course_2),
    3:lambda:tmpfun(usr[0].course_3),
    4:lambda:tmpfun(usr[0].course_4),
    5:lambda:tmpfun(usr[0].course_5),
    6:lambda:tmpfun(usr[0].course_6),
    7:lambda:tmpfun(usr[0].course_7),
    8:lambda:tmpfun(usr[0].course_8),
    9:lambda:tmpfun(usr[0].course_9),
    10:lambda:tmpfun(usr[0].course_10),
    11:lambda:tmpfun(usr[0].course_11),
    12:lambda:tmpfun(usr[0].course_12),
    13:lambda:tmpfun(usr[0].course_13),
    14:lambda:tmpfun(usr[0].course_14),
    15:lambda:tmpfun(usr[0].course_15),
    16:lambda:tmpfun(usr[0].course_16),
    17:lambda:tmpfun(usr[0].course_17),
    18:lambda:tmpfun(usr[0].course_18),
    }[t]()
    return course

def GetKBByDay(usrname,day):
    usr=KB.objects.filter(id_wx=usrname)
    
    def tmpfun(x):
        return x
    
    course = {
    1:lambda:tmpfun(usr[0].course_1+u'\n'+usr[0].course_6+u'\n'+usr[0].course_11),
    2:lambda:tmpfun(usr[0].course_2+u'\n'+usr[0].course_7+u'\n'+usr[0].course_12),
    3:lambda:tmpfun(usr[0].course_3+u'\n'+usr[0].course_8+u'\n'+usr[0].course_13),
    4:lambda:tmpfun(usr[0].course_4+u'\n'+usr[0].course_9+u'\n'+usr[0].course_14),
    5:lambda:tmpfun(usr[0].course_5+u'\n'+usr[0].course_10+u'\n'+usr[0].course_15),
    6:lambda:tmpfun(usr[0].course_16),
    7:lambda:tmpfun(usr[0].course_17),
    8:lambda:tmpfun(usr[0].course_18),
    }[day]()
    
    return course



def CheckIfUserExitInKeBiao(username):

    users= KB.objects.all()
    wx_id_list=[]
    for item in users:
        wx_id_list.append(item.id_wx)
    
    #courses = WebCrawler_KeBiao.KeBiao(213102847)
    
    if username not in wx_id_list:
        ykt = GetYKT(username)
        courses = KeBiao(ykt)
        KB.objects.create(id_wx=username ,course_1=courses[0],course_2=courses[1],course_3=courses[2], \
        course_4=courses[3],course_5=courses[4],course_6=courses[5],course_7=courses[6],course_8=courses[7], \
        course_9=courses[8],course_10=courses[9],course_11=courses[10],course_12=courses[11],course_13=courses[12],\
        course_14=courses[13],course_15=courses[14],course_16=courses[15],course_17=courses[16],course_18=courses[17])
        return False
    else:
        return True


# #######  时间转换，服务器得到的是美国时间  #######
def GetHour(delta):
    d=time.localtime(time.time())
    h=(d.tm_hour+delta)%24
    return h

def GetWeekDay(delta):
    d=time.localtime(time.time())
    w=d.tm_wday+1+(d.tm_hour+delta)/24
    w=w%7
    if w==0:
        return 7
    else:
        return w

def GetMin():
    d=time.localtime(time.time())
    return d.tm_min


# ##############################




def GetKBOfToday(usrname):
    users =KB.objects.filter(id_wx = usrname)
    weekday=GetWeekDay(0)

    def tmpfun(x):
        
        courses=GetKBByDay(usrname,x)
        course_list=courses.split('\n')
        try:
            course_list.remove('')
        except:
            print 'no blank'
        course_list=CleanCourseList(course_list)
        for i in range(len(course_list)):
            course_list[i]+='\n\n'
        return ''.join(course_list)
        
    course={
    1:lambda:tmpfun(1),
    2:lambda:tmpfun(2),
    3:lambda:tmpfun(3),
    4:lambda:tmpfun(4),
    5:lambda:tmpfun(5),
    6:lambda:tmpfun(6),
    7:lambda:tmpfun(7),
    }[weekday]()
    
    return course
    
    
def GetKBOfTomorrow(usrname):
    users =KB.objects.filter(id_wx = usrname)
    weekday=GetWeekDay(0)

    def tmpfun(x):
        courses=GetKBByDay(usrname,x)
        course_list=courses.split('\n')
        try:
            course_list.remove('')
        except:
            print 'no blank'
        course_list=CleanCourseList(course_list)
        for i in range(len(course_list)):
            course_list[i]+='\n\n'
        return ''.join(course_list)

    
    course={
    1:lambda:tmpfun(2),
    2:lambda:tmpfun(3),
    3:lambda:tmpfun(4),
    4:lambda:tmpfun(5),
    5:lambda:tmpfun(6),
    6:lambda:tmpfun(7),
    7:lambda:tmpfun(1),
    }[weekday]()
    
    return course

def CleanCourseList(li_course):
    cleaned_course_list=[]
    cleaned_course_list2=[]

    days = (datetime.date.today() - NewTermDate).days
    weeknum = 1 + days/7 
    
    if weeknum % 2 == 1:
        for cou in li_course:
            if not re.search(u'(双)',cou):
                cleaned_course_list.append(cou)
    else:
        for cou in li_course:
            if not re.search(u'(单)',cou):
                cleaned_course_list.append(cou)
    try:
        for cour in cleaned_course_list:
            tmp_r=re.findall(r'\[[\d]{1,2}\-[\d]{1,2}周\]',cour)
            tmp_s=re.findall(r'[\d]{1,2}',tmp_r[0])
            begin_w = int(tmp_s[0])
            end_w = int(tmp_s[1])
            if weeknum >=begin_w and weeknum <= end_w:
                cleaned_course_list2.append(cour)
    except :
        cleaned_course_list2=cleaned_course_list
    
    return cleaned_course_list2
    
    

def GetNextCourse(usrname):
    w=GetWeekDay(0)
    h=GetHour(0)
    m=GetMin()
    courses=u''
    
    if h<9 or (h==9 and m<45):
        courses=GetSingualKB(usrname,w)+GetSingualKB(usrname,w+5)+GetSingualKB(usrname,w+10) 
    elif h<15 or (h==15 and m<45):
        courses=GetSingualKB(usrname,w+5)+GetSingualKB(usrname,w+10)
    elif h<18 or (h==18 and m<30):
        courses=GetSingualKB(usrname,w+10)
    li_course=courses.split('\n')
    try:
        li_course.remove('')
    except Exception,e:
        print 'no blank'
    
    #d=time.localtime(time.time())
    #return '%d %d %d %d %d'%(d.tm_year,d.tm_mon,d.tm_mday,d.tm_hour,d.tm_min)
        
    li_course=CleanCourseList(li_course)
    
    if len(li_course)==0:
        return ''
    
    #d=time.localtime(time.time())
    #return '%d %d %d'%(GetWeekDay(),GetHour(),GetMin())
        
    else:
        if h<8:
            return li_course[0]
        if h<9 or (h==9 and m<45):
            if re.search(u'1-2节',li_course[0]):
                if len(li_course)==1:
                    return ''
                else:
                    return li_course[1]
            else:
                return li_course[0]
        if h<14:
            return li_course[0]
        
        if h<15 or (h==15 and m<45):
            if re.search(u'6-7节',li_course[0]):
                if len(li_course)==1:
                    return ''
                else:
                    return li_course[1]
            else:
                return li_course[0]
        if h<18 or (h==18 or m<30):
            if len(li_course)==0:
                return ''
            else:
                return li_course[0]
        else:
            return ''
        
        
def UpdateKeBiao(usrname):
    usrs = UserInfo.objects.filter(id_wx = usrname)
    if usrs:
        if usrs[0].id_ykt != None:
            ykt=usrs[0].id_ykt
            #CheckIfUserExitInKeBiao(usrname)
            if CheckIfUserExitInKeBiao(usrname): 
                courses = KeBiao(ykt)
                
                KB.objects.filter(id_wx=usrname).update(course_1=courses[0],course_2=courses[1],course_3=courses[2], \
                course_4=courses[3],course_5=courses[4],course_6=courses[5],course_7=courses[6],course_8=courses[7], \
                course_9=courses[8],course_10=courses[9],course_11=courses[10],course_12=courses[11],course_13=courses[12],\
                course_14=courses[13],course_15=courses[14],course_16=courses[15],course_17=courses[16],course_18=courses[17])
                
def UpdateAllKeBiao():
    users=UserInfo.objects.all()
    if users:
        for item in users:
            UpdateKeBiao(item.id_wx)    
            
        
        
#  ###########  图书馆蛋疼的书名编码转换    ##########
'''
def KillStrangeCoding(original_str):
    replaced_str=original_str.replace('&#x','%u').replace(';','').replace('/','').replace('%u','\\u')
    result=urllib.unquote(replaced_str).decode('unicode-escape')
    print result

'''
# ##########################

def GetCurrentTime():
    w=GetWeekDay(0)
    h=GetHour(0)
    m=GetMin()
    t=u'%s %s %s'%(w,h,m)
    return t



    
    
    
    
    
    

    



    



