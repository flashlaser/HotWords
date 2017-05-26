# coding=utf-8

import fasttext

if __name__=='__main__':
    trainDataPath='../../../data/fasttext/result.txt'
    modelSkipgramPath='../../../data/fasttext/model_skipgram'

    # modelSkipgram=fasttext.skipgram(trainDataPath, modelSkipgramPath)
    modelSkipgram=fasttext.load_model(modelSkipgramPath+'.bin')
    for e in modelSkipgram.words:
        print e