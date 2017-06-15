# coding=utf-8
import re
import time
import urllib
import requests


if __name__ == '__main__':
    out_file=open('/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/users_level_filter', 'w')
    users_blank_set=set()

    for line in open('/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/user_black_uid.dat', 'r').readlines():
        uid=line.strip().strip('\n')
        users_blank_set.add(uid)

    for line in open('/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/users_level', 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        uid=items[0]
        level=items[1]
        if uid in users_blank_set:
            pass
        else:
            out_file.write(line+'\n')
    out_file.close()