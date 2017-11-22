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
#d = dict()
#def f():
#    for i in range(0, 10):
#        for j in range(0, 12345):
#            if i not in d:
#                d[i] = dict()
#            if j % 10 not in d[i]:
#                d[i][j % 10] = 1
#            else:
#                d[i][j % 10] += 1
#f()
#for x,y in d.items():
#    print(y)

#def a(x):
#    print("func a: x = %d" % x)
#
#def b(y):
#    print("func b: y = %d" % y)
#
#func_list = {
#    'a': a,
#    'b': b,
#}
#s = ['a', 'b']
#for x in range(0, 2):
#    func_list[s[x]](x)
#print(func_list)

#a = []
#for x in range(10, -1, -1):
#    for y in range(4):
#        a.append((x, y + 1))
#
#print(sorted(a))
#a.append((-1, 0))
#print(sorted(a))

#cc = [1, 2, 3, 4]
#print(cc)
#cc.insert(0, -1)
#cc.insert(len(cc), 5)
#print(cc)

#a = '[\u00b7\u00d7\u2014\u2018\u2019\u201c\u201d\u2026\u3001\u3002\u300a' \
#    '\u300b\u300e\u300f\u3010\u3011\uff01\uff08\uff09\uff0c\uff1a\uff1b\uff1f]'
#import re
#if re.match(a, '……'):
#    print('YES')

kk = []
for x in range(0, 5):
    kk.insert(0, x)
print(kk)

