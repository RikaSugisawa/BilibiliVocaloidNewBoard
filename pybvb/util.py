# -*- coding: utf-8 -*-
import urllib.request
import json
import time
import datetime



###There are only Chinese notes since the author is too lazy to translate them.
###After all, there will be few people reading this code.╮(╯▽╰)╭
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
    url = 'http://search.bilibili.com/ajax_api/video?keyword=VOCALOID%E4%B8%AD%E6%96%87%E5%8E%9F%E5%88%9B%E6%9B%B2&o' \
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
    daySc, totalSc = get_score(view, danmaku, comment, favorite, mTimeStamp)
    RS.append([nr, title, up, daySc, str(int(totalSc)), str(view), str(danmaku), str(comment), str(favorite),
                   str(coin), mtime, str(GetNowTimeTx())])  # 结果写入list
    #time.sleep(1)
    return 0