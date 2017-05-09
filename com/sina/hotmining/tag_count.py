# coding=utf-8

import sys
import re
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')


## 获取包含警号的话题标签，返回元组类型
def get_siren_content(file_path):
    tag_dic = {}
    pattern = re.compile('#(.*?)#')
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
                tag = tag.strip()
                if tag:
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
        else:
            pass
    # 对字典排序返回的是元组类型
    tag_dic_sort = sorted(tag_dic.items(), lambda x, y: cmp(x[1][0], y[1][0]), reverse=True)
    return tag_dic_sort  # 返回类型为元组


## 获取标签列表（仅含有标签信息和统计信息）
def get_tag_list_simple(tag_dic, n=3):
    tag_list = []
    for e in tag_dic:
        tag = e[0]
        tag_count = e[1][0]
        # 若标签的数量小于n则淘汰掉
        if tag_count <= n:
            break
        else:
            list = []
            list.append(tag)
            list.append(tag_count)
            tag_list.append(list)
    return tag_list


## 过滤一些无用的话题标签
def tag_filter(file_path, tag_list):
    tag_dic_filter = []
    for line in open(file_path, 'r').readlines():
        line = line.strip().strip('\n')
        tag_dic_filter.append(line)

    tag_list_copy = []
    for i in range(0, len(tag_list)):
        flag = 0  # 标记是否存在广告词
        tag = tag_list[i]
        tag_name = tag[0]
        tag_count = tag[1]
        for item in tag_dic_filter:
            if tag_name.__contains__(item):
                flag = 1
                break
            else:
                pass
        if flag == 0:
            list = []
            list.append(tag_name)
            list.append(tag_count)
            tag_list_copy.append(list)
    return tag_list_copy


## 选出出现次数最多的前n条话题
def get_tag_list_top(tag_dic, n=20):
    tag_dic_size = len(tag_dic)
    if tag_dic_size < n:
        n = tag_dic_size
    else:
        pass

    tag_list = []
    for i in range(0, n):
        tag = tag_dic[i][0]
        tag_count = tag_dic[i][1][0]
        blog = tag_dic[i][1][1]
        for w in blog:
            list = []
            mid = w[0]
            uid = w[1]
            url = w[2]

            list.append(tag)
            list.append(tag_count)
            list.append(mid)
            list.append(uid)
            list.append(url)
            tag_list.append(list)

    return tag_list


## 输出话题标签
def tag_out(file_path, tag_list, n=500):
    tag_list_rows = len(tag_list)
    if tag_list_rows < n:
        n = tag_list_rows
    tag_df = pd.DataFrame(tag_list)
    tag_df_head = tag_df.head(n)
    tag_df_head.to_csv(file_path, index=False, header=False, sep='\t')


if __name__ == '__main__':
    # file_path = '/home/littlebei/program/python/pycharm/HotWords/data/wbcont/test.txt'
    # get_siren_content_inner(file_path)
    filter_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/tag_dic_filter.txt'
    read_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/orginal/20170504/20170504_08.blog'
    write_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/tag_sort_20170504_08_filter.txt'


    tag_dic = get_siren_content(read_path)
    tag_list_simple = get_tag_list_simple(tag_dic)
    tag_list = tag_filter(filter_path, tag_list_simple)
    tag_out(write_path, tag_list)
