# -*- coding: utf-8 -*-

from pybvb.util import *
import json
import datetime
import os


if __name__ == '__main__':

    # number of videos to be retrieved
    video_num = 1000

    savefolder = os.getcwd() + '/'

    ### "encode" is not an valid option of open. Try encoding afterwards.
    # nd=open('.\\Output.csv','w+',encoding='gbk')
    fname_data = 'data' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    nd = open(savefolder + fname_data, 'w+', encoding='utf-8')
    nd.write('AV号,标题,UP主,单位得分,总得分,播放,弹幕,评论,收藏,硬币,投稿时间,统计时间\n')
    global RS  # 用于接受结果的list
    RS = []
    # create log file
    fname_log = 'log' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    f_log = open(savefolder + fname_log, 'w+', encoding='utf-8')

    I = 0
    JUDGE = 0

    search_str = '<a href="http://www.bilibili.com/video/av'
    for i in range(1, 50):  # 遍历50页搜索结果
        pg_msg = 'Now at page: {:d}\n'.format(i)
        print(pg_msg)
        f_log.write(pg_msg)
        pg = json.loads(gethtml(i))  # 取得搜索结果
        html = pg['html']
        buf = 0  # 在html中当前搜索位置置零
        while (html.find(search_str, buf + 1) > 0):  # 如果还能找得到视频(请跳至133行)
            if I == video_num:
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
                os.system(savefolder + fname_data)  # 打开输出文件
                exit()  # 结束运行
            buf = html.find(search_str, buf + 1)
            nr = html[(buf + 41):(buf + 48)]  # 取得av号
            try:
                getss(nr, RS)  # 取得视频信息
                msg = 'OK: {:s}\n'.format(nr)
                print(msg)  # 返回成功
                f_log.write(msg)
                I += 1
                if is_30d_ago(RS):
                    print('30-day limit reached!\n')
                    f_log.write('30-day limit reached!\n')
                    JUDGE = 1
                    del RS[-1]
            except:
                msg = 'Warning: {:s}\n'.format(nr)
                print(msg)  # 报错并跳过
                f_log.write(msg)
                continue
                # Coded by:      RikaSugisawa
                # GitHub:        https://github.com/RikaSugisawa/BilibiliVocaloidNewBoard
                #                @RikaSugisawa @mdw771
                # SinaWeibo:     @理科P @温和的三乙醇胺_TEOA
                # QQ:            471592823
                # Email:         tjj.rikap@gmail.com
                # Bilibili:      理科P
