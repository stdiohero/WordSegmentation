#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/10/23

import os
import re

def FMM_segmentation(sentence, dictionary, width=5):
    """
    前向最大匹配，默认匹配窗口长度为5
    :param sentence:
    :param dictionary:
    :param width:
    :return:
    """
    result = [] #返回结果
    start = 0 # 截取窗口的左端
    while start < len(sentence):
        end = start + width
        if end > len(sentence):
            end = len(sentence)
        #截取窗口的右端

        while start < end:
            sub_s = sentence[start: end]

            if sub_s in dictionary or len(sub_s) == 1:
                result.append(sub_s)
                start = end
                break
            end -= 1

    return result

def BMM_segmentation(sentence, dictionary, width=5):
    """
    后向最大匹配， 默认匹配窗口长度为5
    :param sentence:
    :param dictionary:
    :param width:
    :return:
    """
    result = []
    end = len(sentence)
    while end > 0:
        start = end - width
        if start < 0:
            start = 0

        while start < end:
            sub_s = sentence[start: end]
            if sub_s in dictionary or len(sub_s) == 1:
                result.append(sub_s)
                end = start
                break
            start += 1

    result.reverse()
    return result

def read_dict(filename):
    dictionary = set()
    with open(filename, 'rb') as f:
        while True:
            word = f.readline()
            if not word:
                break
            dictionary.add(word.decode().split()[0]) # 解码之后，将词语后面的换行符'\n'去掉

    return dictionary

def test():
    filename = 'WordDict.txt'
    dictionary = read_dict(filename)
    sentence = '从小学计算机，从小学到中学。'
    seg1 = FMM_segmentation(sentence, dictionary)
    seg2 = BMM_segmentation(sentence, dictionary)
    print(seg1)
    print(seg2)

test()
