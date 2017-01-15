# -*- coding: utf-8 -*-

import urllib.request
import json
import datetime
import os
import time
from sys import platform


def timer(timepoints):
    hr = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    now_time = [hr, min]
    return (now_time in timepoints)



def crawl_data(video_num=1000, day_limit=30, timeout=None):

    t0 = time.time()
    savefolder = '{:s}/{:s}/'.format(pwd(), GetNowDateTx().replace(':', '-'))

    if not os.path.exists(savefolder):
        os.mkdir(savefolder)

    fname_data = 'data_' + GetNowTimeTx().replace(':', '-') + '.csv'
    nd = open(savefolder + fname_data, 'w+', encoding='gbk')
    nd.write('AV号,标题,UP主,单位得分,总得分,播放,弹幕,评论,收藏,硬币,投稿时间,统计时间\n')
    global RS  # 用于接受结果的list
    RS = []
    # create log file
    fname_log = 'log_' + GetNowTimeTx().replace(':', '-') + '.csv'
    f_log = open(savefolder + fname_log, 'w+', encoding='utf-8')
    I = 0
    JUDGE = 0
    search_str = '<a href="//www.bilibili.com/video/av'
    for i in range(1, 50):  # 遍历50页搜索结果
        refr_trials = 0
        while(refr_trials <= 2):
            pg_msg = 'Now at page: {:d}\n'.format(i)
            print(pg_msg)
            f_log.write(pg_msg)
            try:
                #pg = json.loads(gethtml(i))  # 取得搜索结果
                #html = pg['html']
                html = gethtml(i)
                #print(html)
                break
            except:
                html = 'placeholder' + search_str
                refr_trials += 1
                print('Warning: Error retrieving html. Trying again...')
                f_log.write('Warning: Error retrieving html. Trying again...\n')
        if refr_trials >= 2:
            print('Warning: Terminated due to html retrieval error.')
            JUDGE = 1
        buf = 0  # 在html中当前搜索位置置零
        while (html.find(search_str, buf + 1) > -1):  # 如果还能找得到视频(请跳至133行)
            if I >= video_num:
                JUDGE = 1
            if timeout is not None:
                if time.time() - t0 > timeout:
                    JUDGE = 1
            if (JUDGE > 0):  # 若完成搜索
                RS = sorted(RS, key=lambda RS: -RS[3], )  # 按单位得分排序
                for i in range(0, len(RS)):  # 挨个视频
                    RS[i][3] = str(RS[i][3])
                    try:  # 试图写入文件
                        nd.write(','.join(RS[i]))
                    except:  # 写不进去就空着
                        nd.write(',')
                        print('Data not written.', RS[i][0])
                        f_log.write('Data not written: {:s}.\n'.format(RS[i][0]))
                    nd.write('\n')  # 写换行
                nd.write(',统计时间：' + GetNowTimeTx())  # 写入统计(当前)时间
                nd.close()  # 关闭文件
                #os.system(savefolder + fname_data)  # 打开输出文件
                exit()  # 结束运行
            buf = html.find(search_str, buf + 1)
            nr = html[(buf + 36):(buf + 43)]  # 取得av号
            try:
                getss(nr, RS)  # 取得视频信息
                msg = 'OK: {:s}\n'.format(nr)
                print(msg)  # 返回成功
                f_log.write(msg)
                I += 1
                if is_nd_ago(RS, day_limit):
                    print('30-day limit reached!\n')
                    f_log.write('30-day limit reached!\n')
                    JUDGE = 1
                    del RS[-1]
            except Exception as e:
                print(e)
                msg = 'Warning: {:s}\n'.format(nr)
                print(msg)  # 报错并跳过
                f_log.write(msg)
                continue

# -*- coding: utf-8 -*-
import urllib.request
import json
import time
import datetime
import os


def pwd():
    return os.getcwd().replace('\\', '/')

def DaysAgoInt(days):  # 取得30天前时间戳
    return int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=days)).timetuple()))


def GetNowTime():  # 取得当前时间戳
    return int(time.mktime(datetime.datetime.now().timetuple()))


def GetNowTimeTx():  # 取得当前时间文本
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def GetNowDateTx():  # 取得当前日期文本
    return datetime.datetime.now().strftime('%Y-%m-%d')


def req(url):  # 携带UA请求文本
    # Construct header dict.
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'
    return urllib.request.urlopen(urllib.request.Request(url, None, headers)).read().decode()


def gethtml(page):  # 请求搜索结果
    '''
    Construct url pointing to specified search result page with keyword "VOCALOID中文原创曲".

    Parameters
    ----------
    page : int
    Page number to be requested.
    '''
    url = 'http://search.bilibili.com/all?keyword=VOCALOID%E4%B8%AD%E6%96%87%E5%8E%9F%E5%88%9B%E6%9B%B2&o' \
          'rder=pubdate&page=' + str(page) + '&_=1475649909891'
    return req(url)


def get_score(view, danmaku, comment, favorite, mTimeStamp):
    '''
    基本公式
        播放得点＋（评论×25＋弹幕）×修正A＋收藏×修正B
    播放得点
        基础得分=播放
        若基础得分>10000，播放得点=基础得分×0.5+5000
        否则，播放得点=基础得分
        若修正B<10，播放得点=上述播放得点×修正B×0.1
    修正A （四舍五入至小数点后两位）
        （播放得分＋收藏）÷（播放得分＋收藏＋弹幕×10＋评论×20）
        其中播放得分等于修正B>10时的播放得点
    修正B （四舍五入至小数点后两位）
        （收藏÷播放）×450（最大限制值：50） （所有的播放数仅计算站内播放）

    本文字引自萌娘百科/周刊VOCALOID中文排行榜（https://zh.moegirl.org/），文字内容遵守【知识共享 署名-非商业性使用-相同方式共享 3.0】协议。
    单位得分=总得分/已投稿天数
    '''
    playA = (view if view <= 10000 else view * 0.5 + 5000)
    rpA = (playA + favorite) / (playA + favorite + 10 * danmaku + 20 * comment)  # 修正A
    rpB = min(favorite / view * 250, 50)  # 修正B
    scPlay = ((view if view <= 10000 else view * 0.5 + 5000) * rpB * 0.1 if rpB < 10 else (
        view if view <= 10000 else view * 0.5 + 5000))  # 播放得点
    totalSc = scPlay + (25 * comment + danmaku) * rpA + favorite * rpB  # 总得分
    daySc = totalSc / (GetNowTime() - mTimeStamp) * 86400  # 单位得分
    return (daySc, totalSc)


def is_nd_ago(RS, days):
    mtime = RS[-1][-2]
    mTimeStamp = int(time.mktime(time.strptime(mtime, '%Y-%m-%d %H:%M:%S')))  # 投稿日期转为时间戳
    if (mTimeStamp < DaysAgoInt(days)):  # 如果超过30天就中止
        return True
    else:
        return False



def getss(nr, RS):  # 获取视频数据
    '''
    Parameters
    ----------
    nr : str
        Video av number.
    num : int
        Number of videos to be retrieved.
    '''
    global JUDGE  # 是否完成请求的标志
    retry = 0
    while(True):
        try:
            js = json.loads(req(
                'http://api.bilibili.com/archive_stat/stat?callback=jQuery17202070728806148786_1475647238270&aid=' + nr + '&type=text&_=1475647238378'))
            break
        except Exception as e:
            retry += 1
            if retry == 3: raise e
    view = js['data']['view']  # 获取播放、收藏、硬币、弹幕数据
    favorite = js['data']['favorite']
    coin = js['data']['coin']
    danmaku = js['data']['danmaku']
    retry = 0
    while(True):
        try:
            js = json.loads(req(
                'http://api.bilibili.com/x/reply?callback=jQuery172021295901065111744_1475652382382&jsonp=text&type=1&sort=2&oid=' + nr + '&pn=1&nohot=1&_=1475652382486'))
            break
        except Exception as e:
            retry += 1
            if retry == 3: raise e
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
    daySc, totalSc = get_score(view, danmaku, comment, favorite, mTimeStamp)
    RS.append([nr, title, up, daySc, str(int(totalSc)), str(view), str(danmaku), str(comment), str(favorite),
                   str(coin), mtime, str(GetNowTimeTx())])  # 结果写入list
    #time.sleep(1)
    return 0

if __name__ == '__main__':

    crawl_data(video_num=3000, day_limit=30, timeout=14400)

# Coded by:      RikaSugisawa
# GitHub:        https://github.com/RikaSugisawa/BilibiliVocaloidNewBoard
#                @RikaSugisawa @mdw771
# SinaWeibo:     @理科P @温和的三乙醇胺_TEOA
# QQ:            471592823
# Email:         tjj.rikap@gmail.com
# Bilibili:      理科P
