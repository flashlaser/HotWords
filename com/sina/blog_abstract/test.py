# coding=utf-8

import sys
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__=='__main__':
    # text = codecs.open('../test/doc/01.txt', 'r', 'utf-8').read()
    text='21日早上，首都机场一位女乘客在摆渡车上发生心源性猝死，万幸的是，她晕倒在了一堆来自军医院的心内科专家的身旁，几位医生同时进行心肺复苏，经过短暂的心脏按压后心跳有了！从昏迷到心跳恢复，整整20秒[good][good]http://t.cn/RofIjm8'
    tr4w = TextRank4Keyword()

    tr4w.analyze(text=text, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

    print( '关键词：' )
    for item in tr4w.get_keywords(20, word_min_len=1):
        print item.word, item.weight

    print()
    print( '关键短语：' )
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
        print(phrase)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')

    print()
    print( '摘要：' )
    for item in tr4s.get_key_sentences(num=1):
        print item.index, item.weight, item.sentence