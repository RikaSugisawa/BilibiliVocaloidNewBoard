# -*- coding: utf-8 -*-
#from __future__ import print_function
import urllib.request
#import urllib2
import json
import time
import datetime
import os
#import numpy as np


###There are only Chinese notes since the author is too lazy to translate them.
###After all, there will be few people reading this code.╮(╯▽╰)╭ 
def ThirtyDaysAgoInt():  # 取得30天前时间戳
    return int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=30)).timetuple()))


def GetNowTime():  # 取得当前时间戳
    return int(time.mktime(datetime.datetime.now().timetuple()))


def GetNowTimeTx():  # 取得当前时间文本
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def req(url):  # 携带UA请求文本
    # Construct header dict.
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'
    return urllib.request.urlopen(urllib.request.Request(url, None, headers)).read().decode()


def gethtml(page):  # 请求搜索结果
    url = 'http://search.bilibili.com/ajax_api/video?keyword=VOCALOID%E4%B8%AD%E6%96%87%E5%8E%9F%E5%88%9B%E6%9B%B2&o' \
          'rder=pubdate&page=' + str(page) + '&_=1475649909891'
    return req(url)


### "encode" is not an valid option of open. Try encoding afterwards.
#nd=open('.\\Output.csv','w+',encoding='gbk')
nd=open('.\\'+datetime.datetime.now().strftime('%Y-%m-%d')+'.csv','w+',encoding='utf-8')
nd.write('AV号,标题,UP主,单位得分,总得分,播放,弹幕,评论,收藏,硬币,投稿时间,统计时间\n')
global RS  # 用于接受结果的list
RS = []


def getss(nr):  # 获取视频数据
    '''
    Parameters :
    ------------
    nr : str
        Video av number.
    '''
    global JUDGE  # 是否完成请求的标志
    global I #统计数目
    I=I+1
    if(I>=1000):
         JUDGE=1 #爬完1k个收手
    js = json.loads(req(
        'http://api.bilibili.com/archive_stat/stat?callback=jQuery17202070728806148786_1475647238270&aid=' + nr + '&type=text&_=1475647238378'))
    view = js['data']['view']  # 获取播放、收藏、硬币、弹幕数据
    favorite = js['data']['favorite']
    coin = js['data']['coin']
    danmaku = js['data']['danmaku']
    js = json.loads(req(
        'http://api.bilibili.com/x/reply?callback=jQuery172021295901065111744_1475652382382&jsonp=text&type=1&sort=2&oid=' + nr + '&pn=1&nohot=1&_=1475652382486'))
    comment = js['data']['page']['count']  # 获取评论数据
    html = req('http://www.bilibili.com/mobile/video/av' + nr + '.html')
    buf1 = html.find('UP主:') + 5  # 获取UP主数据
    buf2 = html.find('</a>', buf1)
    up = html[buf1:buf2]
    buf1 = html.find('video-title') + 20  # 获取标题
    buf2 = html.find('>', buf1)
    title = html[buf1:buf2 - 1]
    buf1 = html.find('up-time') + 9  # 获取投稿日期
    buf2 = html.find('</span>', buf1)
    mtime = html[buf1:buf2]
    mTimeStamp = int(time.mktime(time.strptime(mtime, '%Y-%m-%d %H:%M:%S')))  # 投稿日期转为时间戳
    if (mTimeStamp < ThirtyDaysAgoInt()):  # 如果超过30天就中止
        JUDGE = 1
    else:
        # 基本公式
        #	播放得点＋（评论×25＋弹幕）×修正A＋收藏×修正B
        # 播放得点
        #	基础得分=播放
        #	若基础得分>10000，播放得点=基础得分×0.5+5000
        #	否则，播放得点=基础得分
        #	若修正B<10，播放得点=上述播放得点×修正B×0.1
        # 修正A （四舍五入至小数点后两位）
        #	（播放得分＋收藏）÷（播放得分＋收藏＋弹幕×10＋评论×20）
        #	其中播放得分等于修正B>10时的播放得点
        # 修正B （四舍五入至小数点后两位）
        #	（收藏÷播放）×450（最大限制值：50） （所有的播放数仅计算站内播放）
        #
        # 本文字引自萌娘百科/周刊VOCALOID中文排行榜（https://zh.moegirl.org/），文字内容遵守【知识共享 署名-非商业性使用-相同方式共享 3.0】协议。
        # 单位得分=总得分/已投稿天数
        # Consider employing numpy for numerical computation or statistical modeling.
        playA = (view if view <= 10000 else view * 0.5 + 5000)
        rpA = (playA + favorite) / (playA + favorite + 10 * danmaku + 20 * comment)  # 修正A
        rpB = min(favorite / view * 250, 50)  # 修正B
        scPlay = ((view if view <= 10000 else view * 0.5 + 5000) * rpB * 0.1 if rpB < 10 else (
        view if view <= 10000 else view * 0.5 + 5000))  # 播放得点
        totalSc = scPlay + (25 * comment + danmaku) * rpA + favorite * rpB  # 总得分
        daySc = totalSc / (GetNowTime() - mTimeStamp) * 86400  # 单位得分
        RS.append((nr, title, up, daySc, str(int(totalSc)), str(view), str(danmaku), str(comment), str(favorite),
                   str(coin), mtime, str(GetNowTimeTx())))  # 结果写入list
        print('OK:', nr)  # 返回成功
    time.sleep(1)
    return 0


if __name__ == '__main__':
    I=0
    for i in range(1, 50):  # 遍历50页搜索结果
        JUDGE = 0
        pg = json.loads(gethtml(i))  # 取得搜索结果
        html = pg['html']
        buf = 0  # 在html中当前搜索位置置零
        while (html.find('http://www.bilibili.com/video/av', buf + 1) > 0):  # 如果还能找得到视频(请跳至133行)
            if (JUDGE > 0):  # 若完成搜索
                RS = sorted(RS, key=lambda RS: -RS[3], )  # 按单位得分排序
                for i in range(0, RS.__len__() - 1):  # 挨个视频
                    for j in range(0, 12):  # 挨个数据
                        if (j != 3):  # 若不是得分项
                            try:  # 试图写入文件
                                nd.write(RS[i][j] + ',')
                            except:  # 写不进去就空着
                                nd.write(',')
                                ### nr undefined here.
                                #print('Warning:', nr)
                                #raise Warning('Data not written.')
                                print('Data not written.',RS[i][0])
                        else:  # 若是得分项
                            nd.write(str(int(RS[i][j])) + ',')  # 转成string再写
                    nd.write('\n')  # 写换行
                nd.write(',统计时间：' + GetNowTimeTx())  # 写入统计(当前)时间
                nd.close()  # 关闭文件
                os.system('.\\Output.csv')  # 打开输出文件
                exit()  # 结束运行
            buf = html.find('http://www.bilibili.com/video/av', buf + 1)  # 向后找两次地址避免重复
            buf = html.find('http://www.bilibili.com/video/av', buf + 1)
            nr = html[(buf + 32):(buf + 39)]  # 取得av号
            try:
                getss(nr)  # 取得视频信息
            except:
                print('Warning:', nr)  # 报错并跳过
                continue
                # Coded by:      RikaSugisawa
                # GitHub:        https://github.com/RikaSugisawa/BilibiliVocaloidNewBoard
                #                @RikaSugisawa @mdw771
                # SinaWeibo:     @理科P @温和的三乙醇胺_TEOA
                # QQ:            471592823
                # Email:         tjj.rikap@gmail.com
                # Bilibili:      理科P