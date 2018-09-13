#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/10/29

import re
import logging
import time
from math import *

def is_chinese(word):
    pattern1 = '[\u4e00-\u9fa5]'
    pattern2 = '[\u0000-\u00FF]'
    if not re.match(pattern1, word) or re.match(pattern2, word):
        return False
    return True

def is_symbol(word):
    pattern = '[\u00b7\u00d7\u2014\u2018\u2019\u201c\u201d\u2026\u3002\u300a' \
            '\u300b\u300e\u300f\u3010\u3011\uff01\uff08\uff09\uff0c\uff1a\uff1b\uff1f\u3001]'
    #update: 包含顿号'、'(u3001),
    #包含 · × — ‘ ’ “ ” … 。 《 》 『 』 【 】 ! （ ） ， ： ； ？、
    if re.match(pattern, word):
        return True
    return False

def seg2word(seg):
    pattern = r'([^ ]*?)/\w' # word patten
    pattern_date = r'\d{8}-\d{2}-\d{3}-\d{3}' # date pattern
    start = 'S'
    end = 'E'
    temp_list = re.findall(pattern, seg)
    temp_list.insert(0, start)
    #句子开头加入开始符号S
    result = []
    #这里用list是为了保存语料的原始信息
    for w in temp_list:
        if re.match(pattern_date, w) or (len(w) == 1 and not is_symbol(w) and not is_chinese(w)):
            continue
        if is_symbol(w):
            result.append(end)
            result.append(start)
            continue
        result.append(w.strip().strip('['))
    return result
    #return a list

def parse_files(filename):
    def update_uni_count(cur_words):
        #用于更新uni_count中每个词语出现的数量
        for word in cur_words:
            uni_count['default'] += 1
            if word not in uni_count:
                uni_count[word] = 0
            uni_count[word] += 1
    def update_bi_count(cur_words):
        #用于计算相邻词语出现的次数，更新bi_count
        #s使用嵌套字典存储
        it_fw = 0
        it_bw = 1
        while it_bw < len(cur_words):
            fw = cur_words[it_fw]
            bw = cur_words[it_bw]
            if fw not in bi_count:
                bi_count[fw] = dict()
            if bw not in bi_count[fw]:
                bi_count[fw][bw] = 0
            bi_count[fw][bw] += 1
            it_bw += 1
            it_fw += 1

    uni_count = dict()
    bi_count = dict()
    word_dict = set()
    uni_count['default'] = 0 #default用来统计出现了多少词
    with open(filename, 'rb') as f:
        while True:
            temp_seg = f.readline()
            if not temp_seg:
                break
            cur_words = seg2word(temp_seg.decode())
            word_dict |= set(cur_words)
            update_uni_count(cur_words)
            update_bi_count(cur_words)

    return word_dict, uni_count, bi_count

def smoothing_func(func_param='laplace'):
    """
    输入为平滑函数名，返回一个平滑函数
    :param func_param:
    :return:
    """
    def laplace_smoothing(word_dict, uni_count, bi_count):
        #P(bw|fw)_laplace = (c(fw, bw) + 1) / (c(fw) + |V|)
        # ARPA, p = log10(P)
        abs_V = len(word_dict)
        P_laplace = dict()
        for fw, bw_dict in bi_count.items():
            for bw, cnt in bw_dict.items():
                if bw not in P_laplace:
                    P_laplace[bw] = dict()
                P_laplace[bw][fw] = log10((cnt + 1) / (uni_count[fw] + abs_V))
        #根据公式的特性，对于未在语料库中出现的二元词组，则其bi-gram的值退化为uni-gram
        P_laplace['default'] = dict()
        for w, cnt in uni_count.items():
            P_laplace['default'][w] = log10((0 + 1) / (cnt + abs_V))
            if w not in P_laplace:
                P_laplace[w] = dict()
            P_laplace[w]['default'] = log10((0 + 1) / (cnt + abs_V))
        return P_laplace

    smoothing_func_list = {
        'laplace': laplace_smoothing,
    }
    return smoothing_func_list[func_param]

def write2file(word_dict, uni_count, bi_count, bi_model, uni_model, dict_save_path):
    laplace_smoothing = smoothing_func()
    p_laplace = laplace_smoothing(word_dict, uni_count, bi_count)

    with open(bi_model, 'wb') as f:
       for bw, fw_list in p_laplace.items():
            for fw, p in fw_list.items():
                str = '%s %s %f\n' % (bw, fw, p)
                f.write(str.encode('utf-8'))

def test():
    filename = r'.\data\199801.txt'
    bi_model = r'.\data\bigram.model'
    uni_model = r'.\data\unigram.model'
    dict_save_path = r'.\data\WordDict.txt'
    print('begin....')
    word_dict, uni_count, bi_count = parse_files(filename)

    write2file(word_dict, uni_count, bi_count, bi_model, uni_model, dict_save_path)

#    with open('bigram.model', 'wb') as f:
#        laplace_smoothing = smoothing_func()
#        p_laplace = laplace_smoothing(word_dict, uni_count, bi_count)
#        for bw, fw_list in p_laplace.items():
#            for fw, p in fw_list.items():
#                print('p(%s|%s) = %f ' % (bw, fw, p), end='')
#                str = '%s %s %f\n' % (bw, fw, p)
#                f.write(str.encode('utf-8'))
#            print('')
start = time.time()
test()
end = time.time()
print('Cost %s...' % (end - start))
