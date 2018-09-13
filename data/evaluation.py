#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/11/29

import time
import re

def calc_cut(sentence):
    seg_index = []
    seg = []
    index = 0
    while True:
        cur_index = index + len(seg_index)
        if cur_index >= len(sentence):
            break
        if re.match(r'\s', sentence[cur_index]) != None:
            seg_index.append(index - 1)
        else:
            index += 1
    seg_index.insert(0, -1)
    for i in range(len(seg_index) - 1):
        seg.append('%s%s' % (seg_index[i], seg_index[i + 1]))
    return seg

def compare_cut(my_seg, std_seg):
    my_cnt = len(my_seg)
    std_cnt = len(std_seg)

    correct_cnt = 0
    for seg in my_seg:
        if seg in std_seg:
            correct_cnt += 1

    P = correct_cnt / my_cnt
    R = correct_cnt / std_cnt
    return P, R

def calc_total(my_result, std_result):
    mySeg_list = []
    stdSeg_list = []
    print('%s: begin to read and calc...' % time.asctime())
    with open(my_result, 'rb') as f:
        for line in f.readlines():
            s = line.decode('gbk').strip()
            mySeg_list.append(calc_cut(s + ' '))
    with open(std_result, 'rb') as f:
        for line in f.readlines():
            s = line.decode('gbk').strip()
            if len(s) <= 0:
                continue
            stdSeg_list.append(calc_cut(s + ' '))

    print('%s: begin to write...' % time.asctime())
    N = len(mySeg_list)
    P_list = [0 for x in range(N)]
    R_list = [0 for x in range(N)]
    with open('P_R.data', 'wb') as f:
        for i in range(N):
            P_list[i], R_list[i] = compare_cut(mySeg_list[i], stdSeg_list[i])
            f.write(('P = %s, R = %s\n' % (P_list[i], R_list[i])).encode('utf-8'))

    P_mean = sum(P_list) / N
    R_mean = sum(R_list) / N
    print('P: %s, R: %s' % (P_mean, R_mean))

def test_all():
    my_out = 'output.txt'
    std_out = 'std_out.txt'
    calc_total(my_out, std_out)

def test():
#    s1 = '德艺双馨 继往开来 '
#    s2 = '德艺双馨 继往开来'
#    cs1 = calc_cut(s1.strip() + ' ')
#    cs2 = calc_cut(s2.strip() + ' ')
#    print(cs1)
#    print(cs2)
#    print(compare_cut(cs1, cs2))
    start = time.time()
    test_all()
    end = time.time()
    print('Cost %s s.. ' % (end - start))

test()

