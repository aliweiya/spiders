##  
目标网站 : https://www.cnblogs.com/ 
使用框架 : scrapy1.7.3 + python3.6.0
##  
输出结果 : 拿到博客园文章列表的：作者，发布时间，评论数，阅读数，标题，推荐数 ，输出到指定地址的mysql数据库中

要求 ： 爬虫可以通过配置参数可以自由爬取第n页的数据
## 
 
反爬栏目 ：

请求头伪造使用依赖库：Chrome 版本的 UserAgent

代理IP ： [代理池] "116.196.90.181:3128" , "212.188.66.218:8080" ,  "194.1.193.226:35646" , 等

注 ： 未发现博客园有针对ip的反爬措施，预留了代理ip模块，待持续运行后处理。


##  
说明 :
  
程序入口 : python3 运行 ./main.py
  
程序输出 : 通过 scrapy 配置文件(settings.py) 配置内容抓取到的信息，并保存到指定 mysql 数据库 

##   

项目目录 :
│&emsp;bokeyuan.sql  # mysql数据库文件
  
│&emsp;main.py       # 程序入口程序，从这里运行
  
│&emsp;scrapy.cfg
      
│
  
└─bokeyuan     # Scrapy爬虫主要内容
  
│&emsp;&emsp;│&nbsp;&nbsp;items.py&emsp;&emsp;# 定义爬取 的数据结构  

│&emsp;&emsp;│&nbsp;&nbsp;middlewares.py       # 爬取中间件  

│&emsp;&emsp;│&nbsp;&nbsp;pipelines.py         # 数据管道
  
│&emsp;&emsp;│&nbsp;&nbsp;settings.py          # 全局配置 文件  

│&emsp;&emsp;│&nbsp;&nbsp;__init__.py
  
│&emsp;&emsp;│
  
│&emsp;&emsp;└─spiders
  
│&emsp;&emsp;&emsp;&emsp;bokeyuanInfo.py  # 博客园爬虫
  
└─proxies  

│&emsp;&emsp;&emsp;&emsp;get_available_proxies.py  # 获取免费IP代理并检测IP代理可用性  

│&emsp;&emsp;&emsp;&emsp;proxies.txt  # 可用IP代理文件
  
│

└─result  # 输出到mysql的截图

&emsp;&emsp;&emsp;&emsp; mysql.png

##    