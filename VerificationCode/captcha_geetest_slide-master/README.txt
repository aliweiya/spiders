滑动验证码 : https://www.geetest.com/demo/slide-popup.html
本机运行环境 : python 3.6.0 详细python配置见 Config/README.txt 文件

使用说明 : 部分环境在滑块识别的时候可能会出现 滑块怪物被怪物吃掉或者网络等问题的 骚扰，程序会自动重复识别

captcha_qq-master项目目录结构

│  README.txt
│
├─captcha_geetest_slide-master
│  │  README.md
│  │
│  ├─geetest_demo
│  │  │  captcha1.png
│  │  │  captcha2.png
│  │  │  geetest_demo.py
│  │  │  yanzhengma1.png
│  │  │  __init__.py
│  │  │
│  │  └─result
│  │          极验.gif
│  │
│  └─geetest_type
│          geetest_slide.py
│          __init__.py
│
└─Config
    │  README.txt
    │
    └─selenium驱动程序
            chromedriver.exe


captcha_qq-master项目目录说明

│  README.txt               # README.txt
│
├─captcha_geetest_slide-master
│  │  README.md                # README.md
│  │
│  ├─geetest_demo
│  │  │  captcha1.png                    # geetest_demo.py 生成的中间滑块图片
│  │  │  captcha2.png                    # geetest_demo.py 生成的中间滑块图片
│  │  │  geetest_demo.py      # 破解极验滑动验证码 https://www.geetest.com/demo/slide-popup.html
│  │  │  yanzhengma1.png                 # geetest_demo.py 生成的中间滑块图片
│  │  │  __init__.py
│  │  │
│  │  └─result               # 滑块破解运行动态图
│  │          极验.gif
│  │
│  └─geetest_type             # 此滑动验证的链接已失效，但此处的代码人具有可参考性
│          geetest_slide.py
│          __init__.py
│
└─Config                   # 程序配置文件目录
    │  README.txt                # 程序配置文件
    │
    └─selenium驱动程序          # selenium的程序
            chromedriver.exe
