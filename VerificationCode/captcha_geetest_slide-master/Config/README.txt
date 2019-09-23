python 版本 : python 3.6.0  x64位
操作系统    : windows10 x64位

第三方依赖 :
  -- Pillow: (依赖包)  # 安装这个包会自动安装 PIL 等依赖库
    Pillow 版本 5.3.0
      安装方式 : pip 安装
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pillow
        (指定版本为3.141.0: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pillow==5.3.0)

  -- selenium : (依赖包)
    selenium 版本 3.141.0
      安装方式 : pip 安装
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ selenium
        (指定版本为3.141.0: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ selenium==3.141.0)

  -- chromedriver (依赖驱动)
    对应模拟器版本及驱动程序:
      本实验 chrome浏览器版本 : 版本 76.0.3809.132（正式版本） （64 位）
      chromedriver 驱动程序 : 76.0.3809.126
      chromedriver 下载地址http://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_win32.zip
      下载后该驱动程序放于 ../python/Scripts/ 目录下



"""
    这个在识别的时候对图片截取的时候应该是跟显示屏幕设置放大倍数是有关系的 ,
    默认采用的是 100% ,如果更改放大倍数可能会导致截图的数据发生不可预料性的变化 , 从而影响识别结果的判断
"""