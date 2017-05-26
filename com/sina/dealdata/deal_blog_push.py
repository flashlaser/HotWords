# coding=utf-8

from com.sina.dealdata import deal_blog_field
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


## 获取最近的以.blog_score_filter结尾的文件
def get_blog_filed_filter_file(base_dir):
    file_list = os.listdir(base_dir)
    blog_field_filter_list = []
    for line in file_list:
        if line.__contains__('.blog_score_filter'):
            items = line.split('.')
            name = int(items[0])
            blog_field_filter_list.append(name)
    blog_field_filter_list.sort(reverse=True)
    return str(blog_field_filter_list[0])


## 将目标文件推送到指定的服务器下
def push_blog_mid_file(blog_mid_path):
    os.system('rsync ' + blog_mid_path + ' 10.73.20.41::shaojie5')


if __name__ == '__main__':
    blog_filed_filter_list_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/orginal/20170510/'

