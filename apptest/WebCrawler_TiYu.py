
# encoding:utf-8

import urllib,urllib2
import cookielib
import sgmllib



def PaoCao(usr,pwd):
    #usr='213111517'
    #pwd='110607'
    
    url_login='http://58.192.114.239:8080/studentLogin.do'
    data={'xh':str(usr),'mm':str(pwd),'method':'login'}
    url_check='http://58.192.114.239:8080/studentQueryListChecks.do?method=listChecks'
    cj=cookielib.CookieJar()
    cjhandler=urllib2.HTTPCookieProcessor(cj)
    opener=urllib2.build_opener(cjhandler)
    urllib2.install_opener(opener)
    
    req_login=urllib2.Request(url_login,urllib.urlencode(data))
    res_login=urllib2.urlopen(req_login)
    #print res_login.info()
    #print res_login.read()
    
    req_check=urllib2.Request(url_check)
    res_check=urllib2.urlopen(req_check)
    #print res_check.info()
    html=res_check.read()
    #print html
    parser = TYHtmlParser()
    parser.feed(html)
    return parser.paocao_num
    
    
class TYHtmlParser(sgmllib.SGMLParser):
    flag=0
    num=0
    paocao_num=0
    def start_td(self,attr):
        if attr == [('class','Content_Form')]:
            self.flag=1
            self.num+=1
    
    def end_td(self):
        self.flag=0
            
    def handle_data(self,text):
        if self.flag == 1 and self.num == 8:
            self.paocao_num = text
    
    
    
    
    
if __name__=='__main__':
    print PaoCao(213110561,213110561)
    #s=str('124')
    #print s
    #2131110561


