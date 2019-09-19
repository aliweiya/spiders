import requests
import re
import json
import time
from requests.exceptions import RequestException


def pattern_compile():
    ranking = '<dd>.*?board-index.*?>(.*?)</i>'
    picture = '.*?data-src="(.*?)"'
    movie_name = '.*?title="(.*?)"'
    star = '.*?class="star">(.*?)</p>'
    releasetime = '.*?class="releasetime">(.*?)</p>'
    score = '.*?class="score".*?class="integer">(.*?)</i>.*?class="fraction">(.*?)</i>.*?</dd>'

    info = ranking + picture + movie_name + star + releasetime + score
    return re.compile(info, re.S)


def get_page(url):
    # 搜狗高速浏览器-代理
    headers = {
        'User-Agent;': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.content.decode('utf-8')
    except RequestException:
        return None


def parse_page(html):
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3].strip()) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4].strip()) > 5 else '',
            'score': item[5].strip()+item[6].strip()
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    global pattern
    pattern = pattern_compile()
    url = 'https://maoyan.com/board/4?offset='+str(offset)

    html = get_page(url=url)
    for item in parse_page(html=html):
        write_to_file(item)


if __name__ == '__main__':
    with open('猫眼电影排名.txt', 'w', encoding='utf-8') as f:
        f.write('')
    for i in range(10):
        main(offset=i*10)
        print('爬取第 {num_page} 页...'.format(num_page=i+1))
        time.sleep(1)
    print('Game Over!')

