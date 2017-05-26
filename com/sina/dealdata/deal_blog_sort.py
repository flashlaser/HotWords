# coding=utf-8

import sys
import pandas as pd
import deal_blog_field

reload(sys)
sys.setdefaultencoding('utf-8')


## 依据微博的所占的热词数量进行排序
def sort_hot_words_count(in_path, out_path):
    blogs=pd.read_table(in_path, names=['mid', 'score', 'count'])
    blogs_sort=blogs.sort(['count', 'score'], ascending=False)
    # print(sort.head())
    blogs_sort.to_csv(out_path, sep='\t', header=False, index=False)


if __name__ == '__main__':
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/20170519_14.blog_sort'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/test1'
    #sort_hot_words_count(in_path, out_path)

    out_path_1='/home/littlebei/program/python/pycharm/HotWords/data/hotming/mid'
    deal_blog_field.get_mid(out_path, out_path_1)
