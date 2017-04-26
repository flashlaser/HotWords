# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__=='__main__':
    dicFile='../../../data/dump/'
    filterFile='../../../data/dump/'
    outFile='../../../data/dump/'

    out=open(outFile, 'w')

    dic={}
    for line in open(dicFile, 'r').readlines():
        words=line.strip().strip('\n').split('\t')
        uid=words[0]     # 用户ID所在的列
        level=words[1]   # 用户等级所在的列
        dic[uid]=level

    for line in open(filterFile, 'r').readlines():
        words=line.strip().strip('\n').split('\t')
        mid=words[0]
        uid=words[1]

        if uid in dic:
            level=dic[uid]
        else:
            level='C5'
        result=mid+'\t'+uid+'\t'+level # 需要输出的内容
        out.write(result+'\n')
    out.close()