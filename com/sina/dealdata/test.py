# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__=='__main__':
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/tag/20170522.tag_keywords_2'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/tag/20170522.tag_keywords_3'
    out_file=open(out_path, 'w')
    for line in open(in_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        tag_id=items[0]
        keywords=items[1]
        keywords_list=keywords.split(' ')
        keywords_top=keywords_list[0:200]
        keywords=' '.join(keywords_top)
        result=tag_id+'\t'+keywords
        out_file.write(result+'\n')
    out_file.close()