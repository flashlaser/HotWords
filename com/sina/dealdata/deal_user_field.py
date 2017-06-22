# coding=utf-8

import sys
import time
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

def get_user_type(uid, tryout=3, timeout=3):
    api = "http://i2.api.weibo.com/2/darwin/platform/object/user_ability_tag.json?"
    params = {"source": 3065133901, "uid": uid}
    for i in xrange(tryout):
        try:
            req = requests.get(api, params=params, timeout=timeout)
            if not req:
                continue
            dic = req.json()
            user_type_list=dic['results']
            type_weight=0.0
            for item in user_type_list:
                temp_weight=item['weight']
                if temp_weight>type_weight:
                    type_name=item['display_name']
                    type_id=item['object_id']
                    type_class=item['object_type']
                    type_weight=temp_weight
            return type_name, type_id, type_class, type_weight
        except Exception, e:
            time.sleep(0.1)
            continue
    return None

def get_users_type(in_path, out_path):
    out_file=open(out_path, 'w')
    for line in open(in_path, 'r'):
        line=line.strip().strip('\n')
        items=line.split('\t')
        uid=items[0]
        type=get_user_type(uid)
        if type is None:
            continue
        else:
            type_name, type_id, type_class, type_weight = type
            result=line+'\t'+type_name+'\t'+type_id+'\t'+type_class+'\t'+str(type_weight)
            out_file.write(result+'\n')
    out_file.close()


if __name__=='__main__':
    # print get_user_type('2265145040')
    in_path='/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/users_level'
    out_path='/data0/shaojie5/littlebei/program/python/pycharm/HotWords/data/hotmining/users_level_type'
    get_users_type(in_path, out_path)