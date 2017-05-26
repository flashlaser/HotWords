# coding=utf-8

from gensim.models import ldamodel
from gensim import corpora
import sys
import gensim

reload(sys)
sys.setdefaultencoding('utf-8')


## 获取训练语料
def get_data_train(in_path):
    data_train=[]
    for line in open(in_path, 'r').readlines():
        line=line.strip().strip('\n')
        words=line.split(' ')
        data_train.append(words)
    return data_train


if __name__ == '__main__':
    data_train_path='/home/littlebei/program/python/pycharm/HotWords/data/lda/result'
    data_train=get_data_train(data_train_path)
    dictionary=corpora.Dictionary(data_train)
    # print(dictionary)
    # for item in dictionary:
    #     print dictionary[item]
    corpus=[dictionary.doc2bow(text) for text in data_train]

    for item in corpus:
        print(item)

    num_topics=2
    lda_model=ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
    for i in range(0, num_topics):
        print(lda_model.print_topic(i))