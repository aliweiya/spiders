"""
模块功能: 爬取微博数据并将其内容保存在数据库中
完成目的: 练习学习使用 Ajax, MongoDB
关键模块:
    from urllib.parse import urlencode
    import requests
    from pyquery import PyQuery as pq
    import pymongo
时间: 2018年3月13日 星期三
地点: 平顶山学院 科技楼609
"""


from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import pymongo

"""
抓取网页数据需要的参数,
请求数据需要的 url
头文件中的 headers
"""
base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(page):
    """
    此函数的功能为抓取网页数据, 并通过参数值(eg. 1,2,3,...)的改变返回特定的网络资源
    :param page: 传递内容为网页的指针页数(eg. 1,2,3,...)
    :return: 从网络端请求的 json文件
    """
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None


def parse_page(json_file):
    """
    函数功能: 对从网页上下载来的数据进行解析
    :param json_file:参数内容为一个可序列化的数组, 此处为json文件
    :return: 返回结果为解析后的列表
    """
    if json_file:
        items = json_file.get('data').get('cards')
        for item in items:
            if item.get('mblog'):
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo


def save_mongo(result):
    """
    此函式的功能为向特定的数据中写特定的数据,
    格式为 save_mongo(result),
    存储通道为 MongoDB 非关系型数据库
    :param result: 接受需要保存的数据
    :return: None
    """
    client = pymongo.MongoClient('mongodb://localhost:27017')

    ''' 打开或创建一个新的数据库 '''
    if not client.get_database('weibo_shisi'):
        database = client["weibo_shisi"]
    else:
        database = client.get_database('weibo_shisi')

    ''' 打开或创建表 '''
    if not database.get_collection('weibo'):
        database.create_collection('weibo')
    collection = database.get_collection('weibo')

    ''' 插入从微博上面爬下来的数据,然后保存到数据库并关闭数据库 '''
    collection.insert_one(result)
    client.close()


if __name__ == '__main__':
    '''
    通过迭代获取多个网页, 然后对网页内容进行解析, 接下来将借些内容保存在数据库中
    '''
    for page in range(1, 11):
        json_file = get_page(page=page)
        results = parse_page(json_file=json_file)
        for result in results:
            print(result)
            save_mongo(result)
