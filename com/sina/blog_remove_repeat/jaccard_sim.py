# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def cal_similarity(one_sentence, two_sentence):
    one_sentence=one_sentence.strip().strip('\n')
    one_words=one_sentence.split(' ')
    one_words_size=len(one_words)

    two_sentence=two_sentence.strip().strip('\n')
    two_words=two_sentence.split(' ')
    two_words_size=len(two_words)

    intersection=[word for word in one_words if word in two_words]
    intersection_size=len(intersection)
    similarity=0.0
    if intersection_size ==0:
        return similarity
    if one_words_size<=two_words_size:
        similarity=float(intersection_size)/float(one_words_size)
    else:
        similarity=float(intersection_size)/float(two_words_size)
    return similarity