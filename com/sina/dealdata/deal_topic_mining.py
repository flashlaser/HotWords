# coding=utf-8

import sys
import re
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')


## 获取字符串中警号之间的内容
def get_siren_content_inner(file_path):
    pattern = re.compile('#(.*?)#')

    with open(file_path, 'r') as f:
        while True:
            line = f.readline()
            if line:
                content_list = pattern.findall(line)
                if content_list:
                    for c in content_list:
                        print(c)
            else:
                break


## 获取包含警号的话题标签，返回元组类型
def get_siren_content(file_path):
    tag_dic = {}
    pattern = re.compile('(#.*?#)')
    for line in open(file_path, 'r').readlines():
        words = line.strip().strip('\n').split('\t')
        mid = words[0]
        uid = words[1]
        url = words[2]
        content = words[3]
        # 返回话题标签集合
        tag_list = pattern.findall(content)
        if tag_list:
            for tag in tag_list:
                list = []
                list.append(mid)
                list.append(uid)
                list.append(url)
                if tag in tag_dic:
                    tags = tag_dic[tag]
                    tags[0] = tags[0] + 1
                    tags[1].append(list)
                else:
                    tags = []
                    blog_list = []
                    blog_list.append(list)
                    tags.append(1)
                    tags.append(blog_list)
                    tag_dic[tag] = tags
        else:
            pass
    # 对字典排序返回的是元组类型
    tag_dic_sort = sorted(tag_dic.items(), lambda x, y: cmp(x[1][0], y[1][0]), reverse=True)
    return tag_dic_sort  # 返回类型为元组


if __name__ == '__main__':
    file_path = '/home/littlebei/program/python/pycharm/HotWords/data/wbcont/test.txt'
    get_siren_content_inner(file_path)
