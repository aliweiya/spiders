# -*- coding: utf-8 -*-
# Author: ElvisCT
# Function: 神奇的数字
# Time: 2019年6月8日


def next_num(num):
    """
    计算下一个预定数字
    :param num: 传输进来上一个数字
    :return: 下一个预定数字
    """
    s = list(str(num))
    num_list = dict()
    for item in s:
        num_list[item] = s.count(item)
    sorted(num_list.items(), key=lambda x: x[1], reverse=True)
    num_list = list(num_list.items())
    result = []
    for item in num_list:
        result.append(str(item[1]))
        result.append(str(item[0]))
    result = "".join(result)
    return result


def main(inp, num=5):
    """
    输入数字列
    :param inp: 第一个开始数字
    :param num: 输出到哪一位
    :return: None
    """
    i = 0  # 计数
    for item in range(num):
        res = next_num(inp)
        inp = res
        i += 1
        print("第 {} 个:".format(i), res)


if __name__ == '__main__':
    # 数字输入
    inp = int(input("请输入数字: "))
    main(inp)

