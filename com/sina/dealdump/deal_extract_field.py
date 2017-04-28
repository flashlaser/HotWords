# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    out = open('/home/littlebei/program/python/pycharm/HotWords/data/dump/result/shishi.txt', 'w')
    inputFile = '/home/littlebei/program/python/pycharm/HotWords/data/dump/shishi.txt'
    for line in open(inputFile, 'r').readlines():
        words = line.strip().strip('\n').split('\t')
        if len(words) == 3:
            mid = words[0]
            title = words[1]
            summary = ' '
            domain = ' '
            uid = ' '
            user_name = ' '
            level = ' '
            url = ' '
            content = words[2]
            extend = ' '
            user_type = ' '
            out.write(mid + '\t' + title + '\t' + summary + '\t' + domain + '\t' + uid + '\t' +
                      user_name + '\t' + level + '\t' + url + '\t' + content + '\t' +
                      extend + '\t' + user_type + '\n')
    out.close()
