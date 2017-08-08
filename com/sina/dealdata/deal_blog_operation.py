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

    read_file=open(out_path, 'r')
    blog_list=read_file.readlines()
    read_file.close()

    out_file=open(out_path, 'w')
    for line in blog_list:
        line=line.strip().strip('\n')
        items=line.split('\t')
        mid=items[0]
        uid=items[1]
        score=items[2][0:8]
        result=mid+'\t'+uid+'\t'+score
        out_file.write(result+'\n')
    out_file.close()


## 将目标文件推送到指定的服务器下
def push_blog_file(blog_mid_path):
    os.system('rsync ' + blog_mid_path + ' 172.16.140.61::yanhui11/push/data/hotspot/')


if __name__=='__main__':
    in_path='/data0/shaojie5/littlebei/data/1500087601.blog_hot'
    out_path='/data0/shaojie5/littlebei/data/1500087601.blog_operation'
    get_mid_uid_score(in_path, out_path)