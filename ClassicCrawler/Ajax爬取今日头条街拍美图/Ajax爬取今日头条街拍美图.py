"""
抓取今日头条街拍美图，然后抓取到的图片去重后分类存放
为了加快效率启动了多进程
"""
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
from threading import Thread

# 在创建二级目录的时候替换掉不合法的字符
table = {ord(f): ord(t) for f, t in zip(
     '\/:*?"<>|',
     '         ')}


def get_page(search_keywords, offset):
    """
    拿到网页源码
    :param search_keywords: 搜索关键字
    :param offset: 页数
    :return: 网页源码
    """
    parse = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': search_keywords,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': '1564026381523',
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(parse)
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'cookies': 'tt_webid=6717435902505895428; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6717435902505895428; __tasessionId=zdwz0ub311564024937321; csrftoken=b6ce86f82f567faf64bb158204495656; UM_distinctid=16c27269f825a-01575e7bd42a6d-e343166-144000-16c27269f83b6; CNZZDATA1259612802=269700703-1564022818-%7C1564022818; s_v_web_id=3eccd9766c9351d14db5bb2487d2b4dc',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json, text/javascript',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            print('请求内容错误')
    except requests.RequestException as e:
        print('Error', e.args)
        return None


def get_image(json):
    """
    拿到图片的信息
    :param json: 获取网页的json数据
    :return: 图片的信息
    """
    if json.get('data'):
        # print(json.get('data'))
        for item in json.get('data'):
            if item.get('image_list'):
                title = item.get('title')
                images = item.get('image_list')
                for image in images:
                    yield {
                        'title': title,
                        'image': image.get('url'),
                    }


def save_image(save_directory, item):
    """
    保存图片
    :param save_directory: 图片保存目录
    :param item: 网页的json数据
    :return: None
    """
    content = save_directory
    if not os.path.exists(content):
        os.mkdir(content)

    # 用图片的标题命名文件夹并替换掉不合法字符
    two_level_directory = item.get('title').translate(table).replace('.', '').strip()
    if not os.path.exists("{0}/{1}".format(content, two_level_directory)):
        os.makedirs("{0}/{1}".format(content, two_level_directory))

    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            image = md5(response.content).hexdigest()
            file_path = '{0}/{1}/{2}.jpg'.format(content, two_level_directory, image)
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    print(image)
                    f.write(response.content)

            else:
                print(file_path)
                print('is already download')

    except requests.ConnectionError as e:
        print('Failed to save image: ', item.get('title'))
        print('Reason: ', e.args)


def main(offset):
    """
    控制分页
    :param offset: 第几页
    :return: None
    """
    search_keywords = '街拍'
    save_directory = 'Ajax爬取今日头条街拍美图'
    json = get_page(search_keywords=search_keywords, offset=offset)
    # print(json)
    for item in get_image(json=json):
        print(item)
        save_image(save_directory, item=item)


GROUP_START = 0
GROUP_END = 1


if __name__ == '__main__':
    pool = Pool(maxtasksperchild=5)  # 进程池 , 最多同时给 5 个进程
    groups = [x*20 for x in range(GROUP_START, GROUP_END)]
    pool.map(main, groups)  # 按顺序执行
    pool.close()
    pool.join()
    # for offset in range(GROUP_START, GROUP_END):
    #     th = Thread(target=main, args=[offset])
    #     th.start()

# [main(x*20) for x in range(GROUP_START, GROUP_END)]

# print(os.path.dirname(__file__))
