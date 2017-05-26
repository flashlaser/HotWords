# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def tag_filter(in_path, target_tag, out_path):
    out_file=open(out_path, 'w')

    # 逐行读取文本的每行数据，减少对内存的使用
    with open(in_path, 'r') as f:
        line=f.readline()
        while line:
            if target_tag in line:
                out_file.write(line)
            else:
                pass
            line = f.readline()
    out_file.close()


if __name__=='__main__':
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/test.tag'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result.tag'
    target_tag='tagCategory'
    tag_filter(in_path, target_tag, out_path)