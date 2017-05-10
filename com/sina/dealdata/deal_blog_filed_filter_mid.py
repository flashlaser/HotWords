# coding=utf-8

import os
import sys
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

## 获取最近的以.blog_score_filter结尾的文件
def get_blog_filed_filter_file(base_dir):
    file_list = os.listdir(base_dir)
    blog_filed_filter_list=[]
    for line in file_list:
        if line.__contains__('.blog_score_filter'):
            items=line.split('.')
            name=int(items[0])
            blog_filed_filter_list.append(name)
    blog_filed_filter_list.sort(reverse=True)
    return str(blog_filed_filter_list[0])

## 获取目标文件blog_filed_filter中的mid
def get_blog_filed_filter_mid(in_path, out_path):
    blog_filed_filter=pd.read_table(in_path, header=None)
    blog_filed_filter_mids=blog_filed_filter.iloc[:, 0]
    blog_filed_filter_mids.to_csv(out_path,index=False, header=False)


## 将目标文件推送到指定的服务器下
def push_blog_filed_filter_mid(blog_filed_filter_mid_path):
    os.system('rsync '+blog_filed_filter_mid_path+' 10.73.20.41::shaojie5')


if __name__ == '__main__':
    blog_filed_filter_list_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/orginal/20170510/'
    blog_filed_filter_name=get_blog_filed_filter_file(blog_filed_filter_list_path)

    blog_filed_filter_path=blog_filed_filter_list_path+blog_filed_filter_name+'.blog_score_filter'
    blog_filed_filter_mid_path=blog_filed_filter_list_path+blog_filed_filter_name+'.blog_score_filter_mid'

    get_blog_filed_filter_mid(blog_filed_filter_path, blog_filed_filter_mid_path)

    push_blog_filed_filter_mid(blog_filed_filter_mid_path)

