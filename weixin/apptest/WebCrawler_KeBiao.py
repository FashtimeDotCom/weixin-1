
#encoding:utf-8

import urllib,urllib2
import cookielib
import sgmllib
import re

def KeBiao(ykt):
    ykt_tmp = str(ykt)
    url_kb="http://xk.urp.seu.edu.cn/jw_service/service/stuCurriculum.action"
    data={'returnStr':'','queryStudentId':ykt_tmp,'queryAcademicYear':'12-13-3'}
    html=urllib2.urlopen(url_kb,urllib.urlencode(data))
    html=html.read()
    #print html
    html=html.replace('''<td rowspan="5" class="line_topleft"" align="center">''', \
    '''<td rowspan="5" class="line_topleft" align="center">''')
    parser=KBParser()
    parser.reset()
    parser.feed(html)
    #print "_______________________________"
    parser.clean_kb()
    return parser.kb
    '''
    for item in parser.kb:
        print item
        print "+++++++++++++++"
    
    print len(parser.kb)  
    '''
    
class KBParser(sgmllib.SGMLParser):
    flag=0
    kb=[]
    weekday=0
    i=1
    def __init__(self):
        self.kb=[]
        self.flag=0
        self.weekday=0
    
    def start_td(self,attr):
        #print attr   
        if attr==[('rowspan', '5'), ('class', 'line_topleft'), ('align', 'center')] \
        or attr==[('class', 'line_topleft'), ('rowspan', '2'), ('align', 'center')] or attr==[('class', 'line_topleft'), ('rowspan', '2'), ('colspan', '5'), ('align', 'center')] :
            self.kb.append('')
            #print attr
            self.flag=1
            
    def end_td(self):
        if self.flag==1:
            self.flag=0
            self.weekday+=1
    def handle_data(self,text):
        if self.flag==1:
            #sprint text,':',len(text)
            
            if self.kb[self.weekday]!='':
                if self.kb[self.weekday][-3:]=='节':
                    self.kb[self.weekday]+=text
                    self.kb[self.weekday]+='\n'
                
                #else:
                #    self.kb[self.weekday]+=text
                elif len(self.kb[self.weekday])>6 and (re.search(u'(单)',self.kb[self.weekday][-7:]) or re.search(u'(双)',self.kb[self.weekday][-7:])):
                    self.kb[self.weekday]+=text
                    self.kb[self.weekday]+='\n'
                else:
                    self.kb[self.weekday]+=text
            else:
                self.kb[self.weekday]+=text
            '''
            if self.i==3:
                self.kb[self.weekday]+=text
                self.kb[self.weekday]+='\n'
                self.i=1
            else:
                self.kb[self.weekday]+=text
                self.i+=1
            '''
    def clean_kb(self):
        try:
            self.kb.remove("下午")
        except:
            print "failed"
            
            
# [('class', 'line_topleft'), ('rowspan', '2'), ('align', 'center')]
# [('class', 'line_topleft'), ('rowspan', '2'), ('colspan', '5'), ('align', 'center')]
#  213110561
#  213123363
if __name__=="__main__":
    kb=KeBiao('213102847')

    kb=kb[2]+kb[7]+kb[12]

    kb_list = kb.split('\n')
    
    for item in kb_list:
        if not  re.search(r'(单)',item):
            print item
        else:
            print '++++++',item,'++++++++++'
    

    



