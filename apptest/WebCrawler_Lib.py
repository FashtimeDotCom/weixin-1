
#encoding:utf8


import urllib,urllib2
import cookielib
import sgmllib
#from tools import KillStrangeCoding

def KillStrangeCoding(original_str):
    import sys
    reload(sys)
    #print sys.getdefaultencoding()
    sys.setdefaultencoding('utf8')
    dealed_str=original_str.replace('&#x','%u').replace(';','').replace('%u','\\u').replace('/','')
    result=urllib.unquote(dealed_str).decode('unicode-escape')
    return result

class Lib():
#def Lib(ykt,pwd):
    ykt=''
    pwd=''
    renderlist=[]
    renderdates=[]
    duedates=[]
    positions=[]
    renews=[]
    
    pwderror = False
    
    def __init__(self,y,p):
        self.ykt=y
        self.pwd=p
        self.CrawRenderList()
    
    def CrawRenderList(self):
        tmp_ykt=str(self.ykt)
        tmp_pwd=str(self.pwd)
        url_lib_login='http://www.lib.seu.edu.cn:8080/reader/redr_verify.php'
        data={'number':tmp_ykt,'passwd':tmp_pwd,'returnUrl':'','select':'bar_no'}
        cj=cookielib.CookieJar()
        cjhandler=urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cjhandler)
        urllib2.install_opener(opener)
        
        req_login=urllib2.Request(url_lib_login,urllib.urlencode(data))
        res_login=urllib2.urlopen(req_login)
        #print res_login.info()
        #print res_login.read()
        import re
        if re.search(r'对不起，密码错误，请查实！',res_login.read()):
            self.pwderror = True
            return
        else:
            url_lib_borrowedlist="http://www.lib.seu.edu.cn:8080/reader/book_lst.php"
            req_borrowedlist=urllib2.Request(url_lib_borrowedlist)
            res_borrowedlist=urllib2.urlopen(req_borrowedlist)
            #print res_borrowedlist.info()
            html=res_borrowedlist.read()
            #print html
            parser=LibParser()
            parser.reset()
            parser.feed(html)
            parser.clean_title()
            self.renderlist=parser.books
            self.renderdates=parser.renderdate
            self.duedates=parser.duedate
            self.position=parser.position
            self.renews=parser.renew

    def GetRenderList(self):
        #self.CrawRenderList()
        return self.renderlist
    
    def GetDuedates(self):
        return self.duedates
    
    
        
    
    
    
class LibParser(sgmllib.SGMLParser):
    flag_books=0
    flag_onetitle=0
    flag_render_and_due=0
    flag_render_or_due=0
    flag_renew=0
    flag_position=0
    
    books=[]
    renderdate=[]
    duedate=[]
    renew=[]
    position=[]
    
    def __init__(self):
        self.books=[]
        self.renderdate=[]
        self.duedate=[]
        self.renew=[]
        self.position=[]
    
    
    def start_td(self,attr):
        if attr==[('bgcolor', '#FFFFFF'), ('class', 'whitetext'), ('width', '40%')]:
            self.flag_books=1
        if attr==[('bgcolor', '#FFFFFF'), ('class', 'whitetext'), ('width', '11%')]:
            self.flag_render_and_due=1
            if self.flag_render_or_due==0:
                self.flag_render_or_due=1
            else:
                self.flag_render_or_due=0
        if attr==[('bgcolor', '#FFFFFF'), ('class', 'whitetext'), ('width', '8%')]:
            self.flag_renew=1
        if attr==[('bgcolor', '#FFFFFF'), ('class', 'whitetext'), ('width', '15%')]:
            self.flag_position=1
    
    def end_td(self):
        self.flag_books=0
        self.flag_render_and_due=0
        #self.flag_render_or_due=0
        self.flag_renew=0
        self.flag_position=0
        
    def start_a(self,attr):
        if self.flag_books==1:
            self.books.append('')
            self.flag_onetitle=1
        
    def end_a(self):
        self.flag_onetitle=0
        
    def handle_data(self,text):
        if self.flag_books==1:
            self.books[-1]+=text
        
        if self.flag_render_and_due==1 and self.flag_render_or_due==1:
            self.renderdate.append(text)
        if self.flag_render_and_due==1 and self.flag_render_or_due==0:
            self.duedate.append(text)
        if self.flag_renew==1:
            self.renew.append(text)
        if self.flag_position==1:
            self.position.append(text)
            
    def clean_title(self):
        for i in range(len(self.books)):
            self.books[i]=KillStrangeCoding(self.books[i])
            
            
        
if __name__=="__main__":
    lib=Lib('213102847','311871')
    #lib.CrawRenderList()
    #li=lib.GetRenderList()
    #print li





