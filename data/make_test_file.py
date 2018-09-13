#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/11/29

import re

def seg2word(seg):
    pattern = r'([^ ]*?)/\w' # word patten
    pattern_date = r'\d{8}-\d{2}-\d{3}-\d{3}' # date pattern
    temp_list = re.findall(pattern, seg)
    result = []
    #这里用list是为了保存语料的原始信息
    for w in temp_list:
        if re.match(pattern_date, w):
            continue
        result.append(w.strip().strip('['))
    return result
    #return a list

def parse_files(filename):
    ret = []
    std = []
    with open(filename, 'rb') as f:
        for line in f.readlines():
            str = line.decode()
            s_list = seg2word(str)
            ret.append(''.join(s_list) + '\n')
            std.append(' '.join(s_list) + '\n')
    return ret, std

file = 'test.txt'
out = 'testData.txt'
std_file = 'std_out.txt'
output, std_out = parse_files(file)

#with open(out, 'wb') as f:
#    for line in output:
#        f.write(line.encode('utf-8'))

with open(std_file, 'wb') as f:
    for line in std_out:
        f.write(line.encode('gbk'))



