# [BilibiliVocaloidNewBoard]
## Bilibili Vocaloid New Orignal Songs Ranking List
## Bilibili上的VOCALOID新曲排行榜

  BilibiliVocaloidNewBoard is an open-source Python package for acquiring data of recently published original Vocaloid China songs from Bilibili.com and generating a ranking list based on a novel scoring algorithm.

  BilibiliVocaloidNewBoard是一个用于从哔哩哔哩获取新发布的Vocaloid中文原创曲信息并使用新算法生成排行榜单的开源Python扩展包.


  The main program fetches videos with tag "VOCALOID原创曲" on Bilibili.com published within the recent 30 days, rate them based on the aforementioned algorithm, and yields a csv file containing a list of songs sorted by score.

  主程序可以从B站上获取含有“VOCALOID原创曲”标签的视频, 使用新算法进行评分, 并将按分数排序的歌单写入一个csv(逗号分隔)文件.


####  Instructions for Installation

  The package works with Python 3.4 or above. We recommend to get the latest Python 3.5 interpretor from Anaconda (https://www.continuum.io/downloads).

  After Python is installed, open https://github.com/RikaSugisawa/BilibiliVocaloidNewBoard in browser, click on [Clone or download], then [Download ZIP].

  Unzip the archive to your local directory. Open CMD (Windows) or Terminal (Linux/MacOS), cd into the directory containing BilibiliVocaloidNewBoard-master, and do

  `pip install BilibiliVocaloidNewBoard-master`

  You may also use the `-e` flag to make the package editable, i.e.:

  `pip install -e BilibiliVocaloidNewBoard-master`


####  安装说明

  该扩展包需要Python 3.4或以上. 我们建议从Anaconda获取最新的Python 3.5解释器(https://www.continuum.io/downloads).

  安装Python后, 在浏览器中打开https://github.com/RikaSugisawa/BilibiliVocaloidNewBoard, 点击[Clone or download], 然后[Download ZIP].

  将压缩包解压到本地目录. 打开命令提示符(Windows下)或Terminal(Linux或MacOS下), cd进入包含BilibiliVocaloidNewBoard-master文件夹的目录, 执行

  `pip install BilibiliVocaloidNewBoard-master`

  如要实现安装后的实时编辑, 可以使用-e选项, 即:

  `pip install -e BilibiliVocaloidNewBoard-master`


  One is welcomed to contact us for either collaboratve contributions to this project or comments, suggestions on coding, algorithm improvement or more.

  只要你想为这个工程做点什么，无论是提供代码方面的或是公式改良方面的建议或是一些其他的，我们都欢迎你和我们联系。

    Contact us: SinaWeibo @理科P
    联系我们:    QQ        471592823
                Bilibili  理科P
                Email     tjj.rikap@gmail.com
