# coding=utf-8

import sys
import jieba
import re

reload(sys)
sys.setdefaultencoding('utf-8')


## 去除标点符号以及特殊字符
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


## 获取停用词表
def get_stopwords():
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/lda/stop_words_1893.txt'
    stopwords=[]
    for line in open(in_path, 'r').readlines():
        stopword=line.strip().strip('\n')
        stopwords.append(stopword)
    return stopwords


## 分词
def seg_zh(in_path, seg_symbol, out_path):
    # 加载停用词
    stopwords=get_stopwords()

    out_file=open(out_path, 'w')
    for line in open(in_path, 'r').readlines():
        sentence=line.strip().strip('\n')
        sentence_filter=filter_symbol(sentence)
        seg_list=jieba.cut(sentence_filter, cut_all=False)
        seg_words=[]
        for word in list(seg_list):
            if word in stopwords:
                continue
            else:
                seg_words.append(word)
        result=seg_symbol.join(seg_words)
        out_file.write(result+'\n')
    out_file.close()

if __name__ == '__main__':
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/lda/test'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/lda/result'
    seg_zh(in_path, ' ', out_path)