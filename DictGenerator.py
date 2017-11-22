#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/10/25

import re

def is_chinese(word):
    pattern1 = '[\u4e00-\u9fa5]'
    pattern2 = '[\u0000-\u00FF]'
    if not re.match(pattern1, word) or re.match(pattern2, word):
        return False
    return True

def is_symbol(word):
    pattern = '[\u00b7\u00d7\u2014\u2018\u2019\u201c\u201d\u2026\u3002\u300a' \
            '\u300b\u300e\u300f\u3010\u3011\uff01\uff08\uff09\uff0c\uff1a\uff1b\uff1f\u3001]'
    #包含 · × — ‘ ’ “ ” … 。 《 》 『 』 【 】 ! （ ） ， ： ； ？、
    if re.match(pattern, word):
        return True
    return False

def seg2word(seg):
    pattern = r'([^ ]*?)/\w' # word patten
    pattern_date = r'\d{8}-\d{2}-\d{3}-\d{3}' # date pattern
    seg_symbol = 'S'
    temp_list = re.findall(pattern, seg)
    result = set()
    for w in temp_list:
        if re.match(pattern_date, w):
            continue
        if len(w) == 1:
            if not is_chinese(w):
                continue
        result.add(w)
    return result
    #return a set

def parse_files(filename):
    word_list = set()
    with open(filename, 'rb') as f:
        while True:
            temp_seg = f.readline()
            if not temp_seg:
                break
            word_list = word_list | seg2word(temp_seg.decode()) #利用集合去重
    input_cache = ''
    for w in word_list:
        input_cache += w.strip().strip('[') + '\n'
    return input_cache

def write_files(output_cache, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(output_cache)


def generator():
    input_name = '199801.txt'
    output_name = 'WordDict.txt'
    output_cache = parse_files(input_name)
    print('End of reading, begin to write file...')
    write_files(output_cache, output_name)
    print('End of writing.')

def test():
    """
    测试生成的词典全不全
    :return:
    """
    file1 = '199801.txt'
    file2 = 'WordDict.txt'
    word_dict = set()
    with open(file2, 'rb') as f:
        while True:
            word = f.readline()
            if not word:
                break
            word_dict.add(word.decode().split()[0])

    with open(file1, 'rb') as f:
        tag = 0
        cnt = 0
        while True:
            line = f.readline()
            if not line or tag >= 1:
                break
            word_list = seg2word(line.decode())

            for w in word_list:
                cnt += 1
                if w not in word_dict:
                    print('#%d: %s not in dict' % (cnt, w))
                    tag += 1
                    break


def find_symbol():
    filename = 'WordDict.txt'
    pattern = '[\u4e00-\u9fa5]'
    symbol = '[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]'
    with open(filename, 'rb') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.decode('utf-8').strip()
            if len(line) == 1:
                if re.match(symbol, line) or not re.match(pattern, line):
                    print(line)


generator()
find_symbol()
