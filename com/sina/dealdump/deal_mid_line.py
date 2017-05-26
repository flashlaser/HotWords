#coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

## 判断mid是否在文件的某一行（改行的长度很长）
if __name__=="__main__":
    filterFile = '../../../data/dump/20170428_10.blog'
    dicFile='../../../data/dump/users_C1-C4_update'
    outFile='../../../data/dump/result/20170428_10_in_C1_C4'

    out=open(outFile, 'w')
    dic_new=set()
    for line in open(filterFile, 'r').readlines():
        line=line.strip().strip('\n').split('\t')
        mid=line[0]
        uid=line[1]
        url=line[2]
        for e in open(dicFile, 'r').readlines():
           if e.__contains__(uid):
                 #dic_new.add(mid)
                 e=e.strip().strip('\n').split('\t')
                 level=e[3]
                 r=mid+'\t'+uid+'\t'+url+'\t'+level+'\n'
                 out.write(r)
                 break
    # for value in dic_new:
    #     out.write(value + '\n')
    out.close()