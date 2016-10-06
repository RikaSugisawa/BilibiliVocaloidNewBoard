# -*- coding: utf-8 -*-
import urllib.request
import json
import time
import datetime
import os

def ThirtyDaysAgoInt():
    return int(time.mktime((datetime.datetime.now() - datetime.timedelta(days = 30)).timetuple()))
def GetNowTime():
    return int(time.mktime(datetime.datetime.now().timetuple()))
def gethtml(page):
    url='http://search.bilibili.com/ajax_api/video?keyword=VOCALOID%E4%B8%AD%E6%96%87%E5%8E%9F%E5%88%9B%E6%9B%B2&order=pubdate&page='+str(page)+'&_=1475649909891'
    return urllib.request.urlopen(url).read()
nd=open('.\\Output.csv','w+',encoding='gbk')
nd.write('AV号,标题,UP主,单位得分,总得分,播放,弹幕,评论,收藏,硬币,投稿时间\n')
global RS
RS=[]
def getss(nr):
    global JUDGE
    js=json.loads(urllib.request.urlopen('http://api.bilibili.com/archive_stat/stat?callback=jQuery17202070728806148786_1475647238270&aid='+nr+'&type=text&_=1475647238378').read().decode())
    view=js['data']['view']
    favorite=js['data']['favorite']
    coin=js['data']['coin']
    danmaku=js['data']['danmaku']
    js=json.loads(urllib.request.urlopen('http://api.bilibili.com/x/reply?callback=jQuery172021295901065111744_1475652382382&jsonp=text&type=1&sort=2&oid='+nr+'&pn=1&nohot=1&_=1475652382486').read().decode())
    comment=js['data']['page']['count']
    html=urllib.request.urlopen('http://www.bilibili.com/mobile/video/av'+nr+'.html').read().decode('utf-8')
    buf1=html.find('UP主:')+5
    buf2=html.find('</a>',buf1)
    up=html[buf1:buf2]
    buf1=html.find('video-title')+20
    buf2=html.find('>',buf1)
    title=html[buf1:buf2-1]
    buf1=html.find('up-time')+9
    buf2=html.find('</span>',buf1)
    mtime=html[buf1:buf2]
    mTimeStamp=int(time.mktime(time.strptime(mtime,'%Y-%m-%d %H:%M:%S')))
    if(mTimeStamp<ThirtyDaysAgoInt()):
        JUDGE=1
    playA=(view if view<=10000 else view*0.5+5000)
    rpA=(playA+favorite)/(playA+favorite+10*danmaku+20*comment)
    rpB=min(favorite/view*250,50)
    scPlay=((view if view<=10000 else view*0.5+5000)*rpB*0.1 if rpB<10 else (view if view<=10000 else view*0.5+5000))
    totalSc=scPlay+(25*comment+danmaku)*rpA+favorite*rpB
    daySc=totalSc/(GetNowTime()-mTimeStamp)*86400
    title.replace(u'\xa0',u' ')
    up.replace(u'\xa0',u' ')
    RS.append((nr,title,up,daySc,str(int(totalSc)),str(view),str(danmaku),str(comment),str(favorite),str(coin),mtime))
    nd.flush()
    print('OK:',nr)
    return 0

for i in range(1,50):
  
    JUDGE=0
    pg=json.loads(gethtml(i).decode())
    html=pg['html']
    buf=0
    while(html.find('http://www.bilibili.com/video/av',buf+1)>0):
        if(JUDGE>0):
            RS=sorted(RS,key=lambda RS:-RS[3],)
            for i in range(0,RS.__len__()-1):
                for j in range(0,11):
                    if (j!=3):
                        try:
                            nd.write(RS[i][j]+',')
                        except:
                            nd.write(',')
                            print('Warning:',nr,nd)
                    else:
                        nd.write(str(int(RS[i][j]))+',')
                nd.write('\n')
            nd.close()
            os.system('.\\Output.csv')
            exit()
        buf=html.find('http://www.bilibili.com/video/av',buf+1)
        buf=html.find('http://www.bilibili.com/video/av',buf+1)
        nr=html[(buf+32):(buf+39)]
        try:
            getss(nr)
        except:
            pass
            print('Warning:',nr)
