腾讯活动验证码 : https://open.captcha.qq.com/online.html
本机运行环境 : python 3.6.0   详细python配置见 Config/README.txt 文件

使用说明 : 部分环境在滑块识别的时候可能会出现 滑块怪物被怪物吃掉或者网络等问题的 骚扰，程序会自动重复识别

captcha_qq-master项目目录结构

├─captcha_qq-master
│  │  anti.py
│  │  baidu_demo.py
│  │  captcha_qq.py
│  │  README.md
│  │  targ.jpg
│  │  temp.jpg
│  │  urlsec_qq.py
│  │
│  ├─image
│  │      bkBlock.png
│  │      slideBlock.png
│  │
│  └─result
│          result.gif
│          netwrong.png
│
└─Config
    │  README.txt
    │
    └─selenium驱动程序
            chromedriver.exe


captcha_qq-master项目目录说明

├─captcha_qq-master
│  │  anti.py               # 对selenium模拟浏览器的一种假伪装，因为有些网站可以做到识别selenium
│  │  baidu_demo.py         # selenium功能测试，测试连接为对简书的访问
│  │  captcha_qq.py         # 腾讯防水墙滑动验证码破解 https://open.captcha.qq.com/online.html
│  │  README.md         # README.md
│  │  targ.jpg                   # urlsec_qq.py生成的中间滑块图片
│  │  temp.jpg                   # urlsec_qq.py生成的中间滑块图片
│  │  urlsec_qq.py               # 腾讯防水墙滑动验证码破解 https://urlsec.qq.com/report.html 准确率相对较较低，容易被吃掉
│  │
│  ├─image                # captcha_qq.py生成的中间滑块图片
│  │      bkBlock.png
│  │      slideBlock.png
│  │
│  └─result               # 滑块破解运行动态图
│          result.gif
│          netwrong.png
│
└─Config                   # 程序配置文件目录
    │  README.txt                # 程序配置文件
    │
    └─selenium驱动程序          # selenium的程序
            chromedriver.exe