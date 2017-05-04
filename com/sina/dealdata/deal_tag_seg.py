# coding=utf-8

import sys
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')

def tag_seg(in_path, out_path):
    out_file=open(out_path, 'w')
    for line in open(in_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        tag_name=items[0]
        tag_count=items[1]
        seg_list=jieba.cut(tag_name, cut_all=False)
        tag_words='\001'.join(seg_list)
        tag=tag_name+'\t'+tag_words+'\t'+str(tag_count)

        out_file.write(tag+'\n')
    out_file.close()


if __name__=='__main__':
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/tag_sort_20170504_08_filter.txt'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/tag_sort_20170504_08_filter_seg.txt'
    tag_seg(in_path, out_path)