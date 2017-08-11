# coding=utf-8

import sys
import requests
import time

reload(sys)
sys.setdefaultencoding('utf-8')

def isIn(mid, tryout=3, timeout=5):

    api = "http://10.85.116.5:9999/push/material/manager/findex?"
    params = {"source": 25257758521, "mids": mid}
    for i in xrange(tryout):
        try:
            req = requests.get(api, params=params, timeout=timeout)
            if not req:
                continue
            dic=req.json()
            mid_status= dic['data'][0]['mid']
            if str(mid_status)==mid:
                return True
        except Exception, e:
            print('get_spammer_api:')
            print(e)
            time.sleep(0.1)
            continue
    return False

def hit_count(in_path):
    mid_list=[]
    for line in open(in_path, 'r').readlines():
        mid=line.strip().strip('\n')
        mid_list.append(mid)

    count=0
    for mid in mid_list:
        if isIn(mid):
            count+=1
    return float(count)/len(mid_list)

if __name__=='__main__':
    print isIn('4138790681123389')
    in_path='/data4/shaojie5/littlebei/data/midfile_new/mids.txt'
    print hit_count(in_path)