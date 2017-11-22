#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/10/23

import os
import re
import queue

def FMM_segmentation(sentence, dictionary, width=10):
    #前向最大匹配，默认匹配窗口长度为5
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

def BMM_segmentation(sentence, dictionary, width=10):
    #后向最大匹配， 默认匹配窗口长度为5
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

def full_segmentation(sentence, dictionary, max_width = 12):
    #全切分策咯，句子长度为N，构建[0, N+1]的序列，利用数对(i, j)表示切分的词语sentence[i:j]
    #返回的seg_pool是按照字典序排序的
    seg_relation = dict()
    seg_pool = []
    k = 0
    maxN = len(sentence)
    while k < maxN:
        seg_relation[k] = []
        end = min(k +max_width, maxN)
        while end > k:
            cur_word = sentence[k:end]
            if cur_word in dictionary or end - k == 1:
                seg_relation[k].append(end)
                seg_pool.append((k, end))
            end -= 1
        k += 1
    return seg_relation

def calc_mp(sentence, dictionary):
    model_name = 'bigram.model'
    model = load_model(model_name)
    seg_relation = full_segmentation(sentence, dictionary)

    maxN = len(sentence)
    INF = float('inf')
    default = 'default'
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
                p = -INF
                if fw in model[bw]:
                    p = model[bw][fw]
                    print('%s %s %f' % (bw, sentence[k:i], p))

                curP = dp[k][i] + p #此处分词的右界为i
                print('----------> %d %d: %f + %f = %f' % (k, i, dp[k][i], p, curP))
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

    return best_seg, dp[maxN - 1][maxN]


def dis_ambiguity(sentence):
    #要求输入的sentence前后加入了S E
    dict_file = 'WordDict.txt'
    dictionary = read_dict(dict_file)
    best_seg, maxP = calc_mp(sentence, dictionary)
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
    filename = 'WordDict.txt'
    dictionary = read_dict(filename)
    sentence = 'S北京邮电大学E'
    sentence2 = 'S中华人民共和国E'
    sentence2 = 'S同胞们朋友们女士们先生们E'
#    seg = full_segmentation(sentence, dictionary)
#    for i, j_list in seg.items():
#        for j in j_list:
#            print('%d %d  %s' % (i, j, sentence[i:j]))
    best_seg, maxP = dis_ambiguity(sentence2)
    print(best_seg)
    print(maxP)
#    seg1 = FMM_segmentation(sentence, dictionary)
#    seg2 = BMM_segmentation(sentence, dictionary)
#    print(seg1)
#    print(seg2)

def test_model():
    model = load_model('bigram.model')
    for bw, fw_list in model.items():
        for fw, p in model[bw].items():
            if bw == 'default' and fw == '中':
                print('%s %s %f' % (bw, fw, p))
                print(model[bw][fw])

test()
