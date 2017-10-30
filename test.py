#!/user/bin/env python3
# -*- coding: utf-8 -*-
# Created by Wang Haoyu on 2017/10/25

def add_set(a, s):
    for x in a:
        s.add(x)
def main():
    s = set()
    a = []
    for x in [1, 2, 3]:
        a.append(x)
        add_set(a, s)
    s2 = set()
    for x in range(4, 7):
        a.append(x)
        add_set(a, s2)

#    print(s <= s2)
#    print(s & s2)
#    print(s | s2)
#    print(s2 - s)

#main()

s = 'hello,你好吗。'
print(s[0:5])
print(s[6:10])
