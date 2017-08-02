# coding=utf-8

import sys
import jieba
import re

reload(sys)
sys.setdefaultencoding('utf-8')


## 去除标点符号以及特殊字符
def filter_symbol(context):
    # http正则表达式规则
    # re_http = re.compile(r'[a-zA-z]+://[^\s]*'.decode('utf-8'))
    # re_http = re.compile(r'(?i)\b((https?|ftp|file)://|(www|ftp)\.)[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$]'.decode('utf-8'))
    re_http = re.compile(r'(?i)((http|https)[:：]?//|(www)\.)[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$]'.decode('utf-8'))
    # 中英文标点符号正则表达式
    re_punc = re.compile(r'[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*🙄“”《》【】：（）]+'.decode('utf8'))

    context = context.decode('utf-8')
    context = context.strip().strip('\n')
    context = re_http.sub('', context)
    context = re_punc.sub('', context)
    return context


## 提取文本中的汉字
def get_zh(context):
    context = context.decode('utf-8')
    context = context.strip().strip('\n')
    # 汉字正则表达式
    re_zh = re.compile(u"([\u4e00-\u9fff]+)")
    context_list = re_zh.findall(context)
    context = ' '.join(context_list)
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
    # in_path='/home/littlebei/program/python/pycharm/HotWords/data/lda/test'
    # out_path='/home/littlebei/program/python/pycharm/HotWords/data/lda/result'
    # seg_zh(in_path, ' ', out_path)

    str = '一辆沧州牌照（冀J-6W5Whttp://t.cn/RKPKTnc女子幸运地倒挂在电缆线上，双腿被电缆线的空隙缠绕着。最终，消防队员将其救下。  http://t.cn/Rokv2OI'
    # sentence = get_zh(str)
    # seg_list = jieba.cut(sentence, cut_all=False)
    # words = ' '.join(seg_list)
    # print(words)
    print filter_symbol(str)