# coding=utf-8

import sys
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    blog = pd.read_table('/home/littlebei/program/python/pycharm/HotWords/data/dump/20170502_15_100.blog',
                         names=['mid', 'uid', 'url'])
    blog_5 = blog.head(5)
    print(blog_5)

    users = pd.read_table('/home/littlebei/program/python/pycharm/HotWords/data/dump/users_C1-C4_update',
                          names=['uid', 'username', 'flag', 'level', 'focus'])
    users_5 = users.head(5)
    print(users_5.iloc[:, [0, 3]])
    users_uid_level = users.iloc[:, [0, 3]]  # 获取第0列和第3列的内容

    blog_users = pd.merge(blog, users_uid_level, on='uid')
    print(blog_users.head(5))

    blog_users.to_csv('/home/littlebei/program/python/pycharm/HotWords/data/dump/result/20170502_15_in_C1_C4.txt',
                      index=False, header=False, sep='\t')
