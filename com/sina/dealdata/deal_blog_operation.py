# coding=utf-8

import sys
import os
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

def get_mid_uid_score(in_path, out_path):
    blogs = pd.read_table(in_path, header=None)
    blogs_mid_uid_score = blogs.iloc[:, [0, 1, 3]]
    blogs_mid_uid_score.to_csv(out_path, index=False, header=False, sep='\t')

## 将目标文件推送到指定的服务器下
def push_blog_file(blog_mid_path):
    os.system('rsync ' + blog_mid_path + ' 172.16.140.61::yanhui11/push/data/hotspot/')


if __name__=='__main__':
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/blog_remove_repeat/1496901001.blog_hot'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/blog_remove_repeat/1496901001.blog_operation'
    get_mid_uid_score(in_path, out_path)