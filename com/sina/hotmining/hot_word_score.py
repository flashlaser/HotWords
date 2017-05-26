# coding=utf-8

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import sys
import jieba
import jieba.analyse
import re

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


## 获取待处理文本
def merge_sentence(context_path, col):
    sentence = ''
    for line in open(context_path, 'r').readlines():
        line = line.strip().strip('\n')
        items = line.split('\t')
        blog_content = items[col]
        context = filter_symbol(blog_content)
        sentence = ' '.join((sentence, context))  # 一句一句的连接
    return sentence


### 提取微博中的热词
## 使用jieba中的tf-idf计算热词分数
def jieba_hot_word_score_tf_idf(sentence, top_k, with_weight, allow_POS=()):
    results_tf_idf = jieba.analyse.extract_tags(sentence, topK=top_k, withWeight=with_weight, allowPOS=allow_POS)
    return results_tf_idf


## 使用jieba中的TextRank计算热词分数
def jieba_hot_word_score_text_rank(sentence, top_k, with_weight, allow_POS=()):
    results_text_rank = jieba.analyse.textrank(sentence, topK=top_k)
    return results_text_rank


## 使用jieba中的tf-idf提取文本中关键字
def jieba_hot_word_tf_idf_text(in_path, out_path):
    out_file=open(out_path, 'w')
    for line in open(in_path, 'r').readlines():
        line=line.strip().strip()
        items=line.split('\t')
        blog_mid=items[0]
        blog_content=items[2]
        # 过滤特殊符号
        sentence=filter_symbol(blog_content)
        # 提取每条微博的关键词
        key_words=jieba.analyse.extract_tags(sentence, topK=20, withWeight=False)
        if key_words:
            words=' '.join(key_words)
            result=blog_mid+'\t'+words
            out_file.write(result+'\n')
        else:
            continue
    out_file.close()


## 使用jieba中的TF-IDF提取list中的关键字
def jieba_hot_word_tf_idf(blog_content_list):
    seg_words_list=[]
    for blog_content in blog_content_list:
        blog_content=blog_content.strip().strip('\n')
        # 过滤特殊符号
        sentence = filter_symbol(blog_content)
        # 提取每条微博的关键词
        key_words = jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
        if key_words:
            seg_words_list.append(key_words)
        else:
            continue
    return seg_words_list


## 使用jieba中的TextRank提取文本中的关键字
def jieba_hot_word_text_rank_text(in_path, out_path):
    out_file = open(out_path, 'w')
    for line in open(in_path, 'r').readlines():
        line = line.strip().strip()
        items = line.split('\t')
        blog_mid = items[0]
        blog_content = items[2]
        # 过滤特殊符号
        sentence = filter_symbol(blog_content)
        # 提取每条微博的关键词
        key_words = jieba.analyse.textrank(sentence, topK=20, withWeight=False)
        if key_words:
            words = ' '.join(key_words)
            result = blog_mid + '\t' + words
            out_file.write(result + '\n')
        else:
            continue
    out_file.close()


## 统计文本中的词频
def count_words_text(in_path, out_path):
    out_file=open(out_path, 'w')
    key_words={}
    for line in open(in_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        words=items[1]
        word_list=words.split(' ')
        # 统计词频
        for word in word_list:
            if word in key_words:
                key_words[word]=key_words[word]+1
            else:
                key_words[word]=1
    # 对生成的词频排序
    key_words_sort=sorted(key_words.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    # 将词频输入到指定的文件中
    for item in key_words_sort:
        key=item[0]
        word=item[1]
        result=key+'\t'+str(word)
        out_file.write(result+'\n')
    out_file.close()


## 统计list中的词频
def count_words(seg_words_list):
    key_words={}
    for seg_words in seg_words_list:
        for word in seg_words:
            if word in key_words:
                key_words[word]=key_words[word]+1
            else:
                key_words[word]=1
    # 对生成的词频排序
    key_words_sort = sorted(key_words.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    key_words_list=[]
    for item in key_words_sort:
        word=item[0]
        word_count=[1]
        key_words_list.append(word)

    return key_words_list


## 取前k个关键词
def keywords_top(key_words_list, top_k):
    return key_words_list[0:top_k]


### 提取微博各个类别中的热词
## 分词
def seg_word(sentence):
    seg_list = jieba.cut(str, cut_all=False)
    seg_str = ' '.join(seg_list)
    return seg_str


## 使用sklearn中的tf-idf提取关键词
def sklearn_cal_hot_word_score_tf_idf(corpus):
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        for j in range(len(word)):
            print word[j], weight[i][j]


if __name__ == '__main__':
    print('start-------')
    blog_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170516/20170516_17.blog_users'

    # print('tf-idf--------------')
    # out_path_tf_idf='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170516/20170516_17.blog_hot_word_tf_idf'
    # out_path__tf_idf_count_words='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170516/20170516_17.blog_hot_word_tf_idf_count'
    # jieba_hot_word_tf_idf(blog_path, out_path_tf_idf)
    # count_words(out_path_tf_idf, out_path__tf_idf_count_words)
    #
    # print('text rank--------------')
    # out_path_text_rank='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170516/20170516_17.blog_hot_word_text_rank'
    # out_path_text_rank_count_words = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170516/20170516_17.blog_hot_word_text_rank_count'
    # jieba_hot_word_text_rank(blog_path, out_path_text_rank)
    # count_words(out_path_text_rank, out_path_text_rank_count_words)

    sentence='线程是程序执行时的最小单位，它是进程的一个执行流，'
    key_words=jieba.analyse.textrank(sentence, topK=10)
    for word in key_words:
        print word

    print(type(key_words))