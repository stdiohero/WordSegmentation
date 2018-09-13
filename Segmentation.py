#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/10/23

import os
import re

def is_LetterOrDigital(s):
    pattern = r'^[0-9a-zA-Z]+$'
    return re.match(pattern=pattern, string=s)

def full_segmentation(sentence, dictionary, max_width = 12):
    #全切分策咯，句子长度为N，构建[0, N+1]的序列，利用数对(i, j)表示切分的词语sentence[i:j]
    seg_relation = dict()
    k = 0
    maxN = len(sentence)
    while k < maxN:
        seg_relation[k] = []
        end = min(k +max_width, maxN)
        while end > k:
            cur_word = sentence[k:end]
            if cur_word in dictionary or end - k == 1 or is_LetterOrDigital(cur_word):
                seg_relation[k].append(end)
            end -= 1
        k += 1
    return seg_relation

def calc_mp(sentence, dictionary):
    model_name = 'bigram.model'
    model = load_model(model_name)
    seg_relation = full_segmentation(sentence, dictionary)

    maxN = len(sentence)
    default = 'default'
    INF = float('inf')
    route = dict() #存储路径
    dp = [[-INF for y in range(0, maxN + 1)] for x in range(0, maxN + 1)] #创建一个(maxN+1)*(maxN+1)的矩阵

    route[(0, 1)] = None #初始化边界条件
    dp[0][1] = 0
    for j in range(2, maxN + 1):
        #从起始符S后的第一个词开始
        for i in range(0, j):
            if j not in seg_relation[i]:
                continue
            #当前词语是否是切分词汇, 按照切分规则，切分词汇一定是词典中的词语
            bw = sentence[i:j]
            if bw not in model:
                bw = default
            maxP = -INF
            pre_node = None
            for k in range(i - 1, -1, -1):
                #k的取值从大到小，这样可以在处理相同分值的切分时，选取最小切分
                if i not in seg_relation[k]:
                    continue
                #此时i等效于j
                fw = sentence[k:i]
                if fw not in model[bw]:
                    fw = default
                curP = dp[k][i] + model[bw][fw] #此处分词的右界为i
#                print('%s -> %s ----------> %d %d: %f + %f = %f' % (fw, bw, k, i, dp[k][i], model[bw][fw], curP))
                if curP >= maxP:
                    maxP = curP
                    pre_node = (k, i)
            dp[i][j] = maxP
            route[(i, j)] = pre_node
#    for k, v in route.items():
#        print('%s -> %s' % (str(k), str(v)))
#        if v:
#            print('%s -> %s' % (sentence[k[0]:k[1]], sentence[v[0]:v[1]]))
#    exit(1)
    best_seg = []
    cur_node = (maxN - 1, maxN)
    while cur_node:
        word = sentence[cur_node[0]:cur_node[1]]
        best_seg.insert(0, word)
        cur_node = route[cur_node]
    final_seg = ''
    for w in best_seg:
        if w != 'S' and w != 'E' and w != ' ':
            final_seg += w + ' '
    return final_seg, dp[maxN - 1][maxN]

def is_symbol(word):
    pattern = '[\u00d7\u2014\u2018\u2019\u201c\u201d\u2026\u3002\u300a' \
            '\u300b\u300e\u300f\u3010\u3011\uff01\uff08\uff09\uff0c\uff1a\uff1b\uff1f\u3001]'
    #update: 包含顿号、(u3001),不包含·(u00b7)
    #包含  × — ‘ ’ “ ” … 。 《 》 『 』 【 】 ! （ ） ， ： ； ？、
    if re.match(pattern, word):
        return True
    return False

def pre_cut(sentence):
    sentence_list = []
    buff = ''
    for w in sentence:
        if is_symbol(w) and len(buff) > 0:
            buff = 'S ' + buff + ' E' + w
            sentence_list.append(buff)
            buff = ''
        else:
            buff += w
    if len(buff) > 0:
        buff = 'S' + buff + 'E'
        sentence_list.append(buff)
    return ''.join(sentence_list)

def cut(text):
    #要求输入的sentence前后加入了S E
    dict_file = 'WordDict.txt'
    dictionary = read_dict(dict_file)
    sentence_list = pre_cut(text)
    best_seg, maxP = calc_mp(sentence_list, dictionary)
    return best_seg, maxP

def load_model(filename):
    model = dict()
    with open(filename, 'rb') as f:
        while True:
            line = f.readline().decode('utf-8')
            if not line:
                break
            line = line.split()
            bw, fw, p = line[0].strip(), line[1].strip(), float(line[2].strip())
            if bw not in model:
                model[bw] = dict()
            model[bw][fw] = p
    return model

def read_dict(filename):
    dictionary = set()
    with open(filename, 'rb') as f:
        while True:
            word = f.readline()
            if not word:
                break
            dictionary.add(word.decode().strip()) # 解码之后，将词语后面的换行符'\n'去掉
    return dictionary

def test():
    test_file = 'testset.txt'
    text = []
    with open(test_file, 'rb') as f:
        for line in f.readlines():
            text.append(line.decode('gbk').strip())

    with open('2017140491.txt', 'wb') as f:
        for s in text:
            result, maxP = cut(s)
            f.write(result.encode('gbk'))
            f.write('\n'.encode('gbk'))

#test()
print(cut('今天好开心呀！'))
