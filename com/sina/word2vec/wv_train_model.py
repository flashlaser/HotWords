# coding=utf-8

import sys
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.models.keyedvectors import KeyedVectors

reload(sys)
sys.setdefaultencoding('utf-8')

def trainModel(rFilePath, wFilePath1, wFilePath2):
    sentences = LineSentence(rFilePath)
    model = Word2Vec(sentences, size=4, window=3, min_count=5)
    model.save(wFilePath1)
    model.wv.save_word2vec_format(wFilePath2, binary=False)


if __name__=='__main__':
    inputData='../../../data/word2vec/result.txt'
    outputData1='../../../data/word2vec/model1'
    outputData2='../../../data/word2vec/model2'

    # trainModel(inputData, outputData1, outputData2)
    model1=Word2Vec.load(outputData1)
    print(model1[u'家属'])

    # model2=Word2Vec.load_word2vec_format(outputData2, binary=False)
    # print(model2.wv['家属'])

    # result=model.most_similar(u'家属')
    # for e in result:
    #     print e[0], e[1]