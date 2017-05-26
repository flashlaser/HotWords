#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
if __name__=="__main__":
    out=open('/data0/weibo_bigdata_vf/shaojie5/littlebei/result_data/filter_0425blog_C.txt', 'w')
    dic_1={}

    for line in open('/data0/weibo_bigdata_vf/shaojie5/littlebei/users_C1-C4_update'):
        arr=line.strip().split('\t')
        mid=arr[0]
        level=arr[3]
        dic_1[mid]=level
    for line in open('/data0/weibo_bigdata_vf/shaojie5/littlebei/20170425.blog'):
        text= line.strip().split('\t')
        mid=text[0]
        uid=text[1]
        url=text[2]
        if dic_1.get(uid):
            level=dic_1.get(uid)
        else:
            level='C5'
        result=mid+'\t'+uid+'\t'+url+'\t'+level
        out.write(result + '\n')
    out.close()