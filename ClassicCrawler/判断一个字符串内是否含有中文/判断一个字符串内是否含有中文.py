# -*- coding: utf-8 -*-

import re

zh_pattern = re.compile('[\u4e00-\u9fa5]+')

def chinese_detection(string_word):
    """
    判断传入字符串，判断是否包含中文
    :param string_word: 传入的要检测的是否含有中文的字符串
    :return: True or False
    """
    if re.search(pattern=zh_pattern, string=string_word):
        return True
    else:
        return False


def main():
    """
    主函数
    :return: None
    """
    while True:
        string_word = input('please input a string: ')
        if string_word == "0000":
            print("########## EXIT ##########")
            exit()
        else:
            result = chinese_detection(string_word=string_word)
            print(string_word)
            if result:
                print('''this string has chinese''')
            else:
                print("""this string don't have chinese""")
        print()


if __name__ == '__main__':
    main()

