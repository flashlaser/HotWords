# coding=utf-8

import sys
import pandas as pd
import re
import jieba
import jieba.analyse

reload(sys)
sys.setdefaultencoding('utf-8')


## 处理特殊符号
def filter_symbol(context):
    # http正则表达式规则
    re_http = re.compile(r'[a-zA-z]+://[^\s]*')
    # 中英文标点符号正则表达式
    re_punc = re.compile('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*🙄“”《》【】：（）]+'.decode('utf8'))

    context = context.decode('utf-8')
    context = context.strip().strip('\n')
    context = re_http.sub('', context)
    context = re_punc.sub('', context)

    return context

def keywords_extract_tf_idf(sentence):
    key_words = jieba.analyse.extract_tags(sentence, topK=15)
    words = ''.join(key_words)
    return words


if __name__=='__main__':
    sentence='#晓说2017#节目神预测！高晓松押中高考题，从预测奥斯卡到预测#高考作文#，江苏高考见证新一代预测帝诞生！说到古今中外未来出行，我只服@高晓松 ，到底矮大紧咋说的？不废话看视频[笑而不语]http://t.cn/Ra1nDIH '
    sentence=filter_symbol(sentence)
    print keywords_extract_tf_idf(sentence)

    sentence = '高晓松押中高考题，就是不知道这一年压了多少个考题。女子面试自称有颜值有气质，哎，狗生如戏，全靠演技，我可能遇到了一只假狗[摊手]#分享南京# http://t.cn/RMFrrlN ​'
    sentence = filter_symbol(sentence)
    print keywords_extract_tf_idf(sentence)