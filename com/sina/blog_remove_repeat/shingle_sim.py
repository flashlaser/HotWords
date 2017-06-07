# -*- coding: utf-8 -*-
# !/usr/bin/python
##################################################
# AUTHOR : Yandi LI
# CREATED_AT : 2015-10-09
# LAST_MODIFIED : 2015年10月09日 星期五 14时10分39秒
# USAGE : python sim.py "中兴华为供应商跑路 制造业寒冬蔓延至手机行业" "中兴华为跑路 制造业寒冬蔓手机行业"
# PURPOSE : Compute shingle similarity of two strings
##################################################

import re

t_space = re.compile(ur'\s', re.UNICODE)


def get_shingles(text, size=3):
    shingles = set()
    for i in range(0, len(text) - size + 1):
        shingles.add(text[i:i + size])
    return shingles

def jaccard(set1, set2):
    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    return x, y


def shingleSimilarity(text1, text2, size=3):
    """Shingle similarity of two texts
    """
    t1 = t_space.sub('', text1.decode('utf8'))
    t2 = t_space.sub('', text2.decode('utf8'))
    x, y = jaccard(get_shingles(t1, size), get_shingles(t2, size))
    #  if len(text1) != len(text2):
    #    tmp=text1.split(' ')
    #    for term in tmp:
    #      if term in text2:
    #        y=y+len(text1)-1
    return x / float(y) if (y > 0 and x > 2) else 0.0


if __name__ == "__main__":
    import sys

    text1 ='高晓松预测高考作文矮大紧只服2017晓说高考题古今中外废话见证奥斯卡高考不语视频'
    text2 ='高晓松如戏摊手假狗颜值哎狗生高考题考题演技面试全靠气质分享自称女子'
    print shingleSimilarity(text1, text2)

