# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

## 找出not_white_list在blog中的数据
if __name__=="__main__":
    dicFile='../../../data/dump/'
    blogFile='../../../data/dump/'
    outFile='../../../data/dump/'

    out=open(outFile, 'w')
    dic=[]
    for line in open(dicFile, 'r').readlines():
        mid=line.strip().strip('\n')  # dicFile中只有一列
        dic.append(mid)               # 将mid放入dic集合中
    for line in open(blogFile, 'r'):
        words=line.strip().strip('\n').split('\t')
        mid=words[0]
        uid=words[1]
        url=words[2]
        if mid in dic:
            out.write(line+'\n')
        else:
            pass
    out.close()