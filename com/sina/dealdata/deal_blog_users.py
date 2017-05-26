# coding=utf-8

import sys
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    blogs = pd.read_table('/home/littlebei/program/python/pycharm/HotWords/data/hotming/orginal/20170516/20170516_17.blog',
                         names=['blog_mid', 'uid', 'blog_content'])
    # blog_mid_uid_url=blogs.iloc[:, [0, 1, 2]]
    # print(blog_mid_uid_url.head(2))
    print(blogs.head(2))

    users = pd.read_table('/home/littlebei/program/python/pycharm/HotWords/data/hotming/users_level',
                          names=['uid', 'user_level'])
    # users_uid_level = users.iloc[:, [0, 3]]  # 获取第0列和第3列的内容

    blog_users = pd.merge(blogs, users, on='uid')
    print(blog_users.head(5))

    blog_users.to_csv('/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170516/20170516_17.blog_users',
                      index=False, header=False, sep='\t')
