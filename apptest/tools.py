
#encoding:utf-8


from models import UserInfo



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



