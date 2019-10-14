import requests
from settings import *
import re
i = 0
try:
    test_url = 'http://zsxx.pdsu.edu.cn/info/1004/1132.htm'
    response = requests.get(test_url, headers=headers, timeout=5)
    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        st = re.findall('<tbody.*?>.*?</tbody>', response.text, re.S)[0]
        trs = re.findall('<tr.*?>.*?</tr>', st, re.S)

        if re.findall('<span.*?>(.*?)</span>', trs[1], re.S):
            num = len(re.findall('<span.*?>(.*?)</span>', trs[1]))
        elif re.findall('<td.*?>(.*?)</td>', trs[1], re.S):
            num = len(re.findall('<td.*?>(.*?)</td>', trs[1]))
        for tr in trs:
            if re.findall('<span.*?>(.*?)</span>', tr, re.S):
                result = re.findall('<span.*?>(.*?)</span>', tr, re.S)
            elif re.findall('<td.*?>(.*?)</td>', tr, re.S):
                result = re.findall('<td.*?>(.*?)</td>', tr, re.S)
            
            if num == 5:
                print(result)
            elif num == 6:
                if len(result) == 5:  # 判断，如果长度为5，说明这个专业分为文理科
                    result.insert(0, major)
                elif len(result) == 6:  # 判断，如果长度为6，可能下一项长度为5或6，就让下一项插入这个的第一项
                    major = result[0]
                print(result)
        print(num)
    else:
        print('hahaha')
        pass
except:
    print('lalala')
    pass