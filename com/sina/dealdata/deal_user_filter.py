# coding=utf-8

import sys
import pandas as pd

reload(sys)

sys.setdefaultencoding('utf-8')


def user_filter_uid(users_level_path, user_black_uid_path, user_level_type_black_path, user_level_filter_path):
    out_file = open(user_level_filter_path, 'w')
    users_blank_set = set()

    for line in open(user_black_uid_path, 'r').readlines():
        uid = line.strip().strip('\n')
        users_blank_set.add(uid)

    for line in open(user_level_type_black_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        uid=items[0]
        users_blank_set.add(uid)

    for line in open(users_level_path, 'r').readlines():
        line = line.strip().strip('\n')
        items = line.split('\t')
        uid = items[0]
        level = items[1]
        if uid in users_blank_set:
            pass
        else:
            out_file.write(line + '\n')
    out_file.close()


def user_filter_type(user_level_type_path, type_black_path, user_level_type_black_path, weight_threshold):
    user_level_type_black_file=open(user_level_type_black_path, 'w')

    type_black_set=set()
    for line in open(type_black_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        type_id=items[0]
        type_black_set.add(type_id)

    for line in open(user_level_type_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        type_id=items[3]
        type_weight=float(items[5])
        if type_id in type_black_set:
            if type_weight>weight_threshold:
                user_level_type_black_file.write(line+'\n')

    user_level_type_black_file.close()


if __name__ == '__main__':
    user_level_type_path='/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/users_level_type'
    type_black_path='/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/user_type_black.txt'
    user_level_type_black_path='/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/user_level_type_black'
    user_filter_type(user_level_type_path, type_black_path, user_level_type_black_path, 80.0)

    users_level_path='/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/users_level'
    user_black_uid_path='/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/user_black_uid.dat'
    user_level_filter_path='/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/users_level_filter'

    user_filter_uid(users_level_path, user_black_uid_path, user_level_type_black_path, user_level_filter_path)