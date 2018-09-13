#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/11/29

origin_file = '199801.txt'
train_file = 'train.txt'
test_file = 'test.txt'

origin_text = []
with open(origin_file, 'rb') as f:
    for line in f.readlines():
        origin_text.append(line.decode().strip())

N = len(origin_text)
n = int(N * 0.8)

with open(train_file, 'wb') as f:
    index = 0
    while index < n:
        f.write(origin_text[index].encode('utf-8'))
        f.write('\n'.encode('utf-8'))
        index += 1

with open(test_file, 'wb') as f:
    index = n
    while index < N:
        f.write(origin_text[index].encode('utf-8'))
        f.write('\n'.encode('utf-8'))
        index += 1
