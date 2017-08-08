# coding=utf-8

from com.sina.giveme import redis_token
import urllib, urllib2
import json
import time
import sys
import redis
import os
import pandas as pd
import re
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


def get_redis():
    # 配置redis
    h0 = 'rs20218.mars.grid.sina.com.cn'
    p0 = '20218'
    db_read_0 = redis.Redis(host=h0, port=p0)

    h1 = 'rs20373.mars.grid.sina.com.cn'
    p1 = '20373'
    db_read_1 = redis.Redis(host=h1, port=p1)

    h2 = 'rs20374.mars.grid.sina.com.cn'
    p2 = '20374'
    db_read_2 = redis.Redis(host=h2, port=p2)

    h3 = 'rs20375.mars.grid.sina.com.cn'
    p3 = '20375'
    db_read_3 = redis.Redis(host=h3, port=p3)

    h4 = 'rs20376.mars.grid.sina.com.cn'
    p4 = '20376'
    db_read_4 = redis.Redis(host=h4, port=p4)

    h5 = 'rs20377.mars.grid.sina.com.cn'
    p5 = '20377'
    db_read_5 = redis.Redis(host=h5, port=p5)

    h6 = 'rs20378.mars.grid.sina.com.cn'
    p6 = '20378'
    db_read_6 = redis.Redis(host=h6, port=p6)

    h7 = 'rs20379.mars.grid.sina.com.cn'
    p7 = '20379'
    db_read_7 = redis.Redis(host=h7, port=p7)

    return db_read_0, db_read_1, db_read_2, db_read_3, db_read_4, db_read_5, db_read_6, db_read_7


## 获取要处理的mid文件
## 参数base_dir：存放mid文件的文件夹
## 返回值：最近文件的第二个文件
def get_mid_file(base_dir):
    file_list = os.listdir(base_dir)
    file_list.sort(reverse=True)
    return file_list[1]


## 获取blog中的mid
def get_mid(in_path, out_path):
    try:
        blogs = pd.read_table(in_path, header=None)
        blog_mids = blogs.iloc[:, 0]
        blog_mids.to_csv(out_path, index=False, header=False)
    except Exception, e:
        print(get_mid, e)


## 获取spammer接口字段
def get_spammer_api(mid, tryout=3, timeout=5):
    api = "http://i.datastrategy.weibo.com/1/strategy/distribution/feed/hot/show.json?"
    params = {"source": 134277248, "mid": mid}
    for i in xrange(tryout):
        try:
            req = requests.get(api, params=params, timeout=timeout)
            if not req:
                continue
            dic=req.json()
            spammer_flag = dic["data"]["result"]['value']
            return spammer_flag
        except Exception, e:
            print('get_spammer_api:')
            print(e)
            time.sleep(0.1)
            continue
    return None


## 获取单条微博中的uid、level、created_at、content、content_length等信息
def get_uid_level_time_content(app_token, mid):
    # url = 'http://i2.api.weibo.com/2/statuses/show_batch.json?source=1586188222&simplify=1&ids=' + mid
    # jsonstr = urllib2.urlopen(url, timeout=5).read()
    # dic = json.loads(jsonstr, strict=False)

    api_url = 'http://i2.api.weibo.com/2/statuses/show_batch.json?'
    params = {"source": 1586188222, 'simplify': 1, 'ids': mid, "app_token": app_token}

    for i in xrange(5):
        try:
            req = requests.get(api_url, params=params, timeout=5)
            if not req:
                continue
            dic = req.json()
            blog_uid = str(dic['statuses'][0]['user']['id'])  # json 文件中的uid字段是int类型
            blog_created_at = dic['statuses'][0]['created_at']
            blog_content = dic['statuses'][0]['text']
            blog_content = blog_content.replace('\n', '')
            blog_content_length = dic['statuses'][0]['textLength']
            return blog_uid, blog_content, blog_created_at, blog_content_length
        except Exception, e:
            print('get_uid_level_time_content:')
            print(e)
            time.sleep(0.1)
            continue
    return None


## 获取单条微博的tag_id, tag_name
def get_tag(app_token, mid):
    # url = 'http://i.api.weibo.com/2/darwin/platform/object/content_tag.json?source=646811797&content_type=1&content_id=' + mid
    # jsonstr = urllib2.urlopen(url, timeout=5).read()
    # dic = json.loads(jsonstr, strict=False)

    api_url = 'http://i.api.weibo.com/2/darwin/platform/object/content_tag.json?'
    params = {"source": 646811797, 'content_type': 1, 'content_id': mid, "app_token": app_token}

    for i in xrange(5):
        try:
            req = requests.get(api_url, params=params, timeout=5)
            if not req:
                continue
            dic = req.json()
            topic_list = dic['results']

            tag_id = ' '
            tag_name = ' '
            tag_weigth = 0.0
            for item in topic_list:
                if 'object_type' in item:
                    if item['object_type'] == 'tagCategory':
                        temp_weigth=item['weight']
                        if temp_weigth>tag_weigth:
                            tag_id = item['object_id']
                            tag_name = item['display_name']
                            tag_weigth=temp_weigth
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            return tag_id, tag_name
        except Exception, e:
            print(e)
            time.sleep(0.1)
            continue
    return None


## 获取单条blog中的video
def get_video(blog_content):
    flag = 0
    try:
        # 匹配http链接规则
        pattern_http = re.compile(r'http://[\S]+')
        https = re.findall(pattern_http, blog_content)
        if https and len(https) > 0:
            video_url = 'http://i2.api.weibo.com/2/short_url/info.json?source=646811797&url_short=' + https[
                len(https) - 1]
            video_json = urllib2.urlopen(video_url, timeout=5).read()
            video_dic = json.loads(video_json, strict=False)

            url_long = video_dic['urls'][0]['url_long']
            url_type = video_dic['urls'][0]['annotations'][0]['object_type']

            if url_long.find('miaopai') != -1 or (url_type == 'video' and 'video.weibo.com/show' in url_long):
                flag = 1
            else:
                pass
        else:
            pass
    except Exception, e:
        print('get_video:')
        print(e)
    finally:
        return flag


## 获取单条微博的转评赞
def get_like_comments_repost(app_token, mid):
    api_url = 'http://i2.api.weibo.com/2/statuses/count_sp.json?'
    params = {"source": 1586188222, 'ids': mid, "app_token": app_token}

    for i in xrange(5):
        try:
            req = requests.get(api_url, params=params, timeout=5)
            if not req:
                continue
            dic = req.json()
            reads = dic[0]['reads']  # 阅读量
            reposts = dic[0]['reposts']  # 转发量
            attitudes = dic[0]['attitudes']  # 点赞数
            comments = dic[0]['comments']  # 评论
            return reads, reposts, attitudes, comments
        except requests.RequestException:
            time.sleep(0.1)
            continue
    return 0, 0, 0, 0


## 获取批量转评赞
def get_like_comments_repost_batch(app_token, mid_list):
    mids = ','.join(mid_list)
    api_url = 'http://i2.api.weibo.com/2/statuses/count_sp.json?'
    params = {"source": 1586188222, 'ids': mids, "app_token": app_token}

    blog_information_list = []
    for i in xrange(5):
        try:
            req = requests.get(api_url, params=params, timeout=5)
            if not req:
                continue
            dic = req.json()
            for j in range(0, len(mid_list)):
                try:
                    blog_information = []
                    mid = mid_list[j]
                    reads = dic[j]['reads']  # 阅读量
                    reposts = dic[j]['reposts']  # 转发量
                    attitudes = dic[j]['attitudes']  # 点赞数
                    comments = dic[j]['comments']  # 评论

                    blog_information.append(mid)
                    blog_information.append(reads)
                    blog_information.append(reposts)
                    blog_information.append(attitudes)
                    blog_information.append(comments)

                    blog_information_list.append(blog_information)
                except Exception, e:
                    print('get_like_comments_repost_batch'+e)
                    continue
            return blog_information_list
        except requests.RequestException:
            time.sleep(0.1)
            continue
    return None


## 获取互动曝光比
## 参数mid
## 返回值:互动数,曝光数,互动曝光比
def get_act_expose_rate(mid, db_read_0, db_read_1, db_read_2, db_read_3, db_read_4, db_read_5, db_read_6, db_read_7):
    db = None
    try:
        if int(mid) % 8 == 0:
            db = db_read_0
        elif int(mid) % 8 == 1:
            db = db_read_1
        elif int(mid) % 8 == 2:
            db = db_read_2
        elif int(mid) % 8 == 3:
            db = db_read_3
        elif int(mid) % 8 == 4:
            db = db_read_4
        elif int(mid) % 8 == 5:
            db = db_read_5
        elif int(mid) % 8 == 6:
            db = db_read_6
        elif int(mid) % 8 == 7:
            db = db_read_7
    except Exception, e:
        print('get_act_expose_rate', e)
        return 0, 0, 0.0

    action = 0
    expose = 0
    rate = 0.0
    num = 0
    while num < 1:
        num += 1
        try:
            mid_expose = mid + '#exposure2'
            if db.exists(mid_expose) == False:
                expose = 0
            else:
                expose = int(db.get(mid_expose))
            mid_action = mid + '#action2'
            if db.exists(mid_action) == False:
                action = 0
            else:
                action = db.pfcount(mid_action)
        except Exception, e:
            print('get_act_expose_rate', e)
            continue
    # rate为互动曝光比
    rate = (float(int(action) + 1)) / float((int(expose) + 1))
    return action, expose, rate


## 获取离线数据中blog的各个字段
def get_all_field(mid_path, out_path):
    out = open(out_path, 'w')
    for line in open(mid_path, 'r').readlines():
        line = line.strip().strip('\n')
        words = line.split('\t')
        mid = words[0]
        uid = words[1]
        url = words[2]
        level = words[3]
        reads, reposts, attitudes, comments = get_like_comments_repost(mid)
        action, expose, rate = get_act_expose_rate(mid)
        result = mid + "\t" + uid + "\t" + url + "\t" + level + "\t" + str(reads) + "\t" + str(reposts) + "\t" + str(
            attitudes) + "\t" + str(comments) + "\t" + str(action) + "\t" + str(expose) + "\t" + str(rate)
        out.write(result + '\n')
    out.close()


## 获取流数据中的各个字段reads,reposts,attitudes,attitudes,comments,action,expose,rate
def get_blog_field_streaming(app_token, mid_path, out_path):
    # 加载mid
    out = open(out_path, 'w')
    mid_set = set()
    for line in open(mid_path, 'r').readlines():
        mid = line.strip().strip('\n')
        mid_set.add(mid)

    for mid in mid_set:
        reads, reposts, attitudes, comments = get_like_comments_repost(mid, app_token)
        action, expose, rate = get_act_expose_rate(mid)
        result = str(mid) + '\t' + str(reads) + "\t" + str(reposts) + "\t" \
                 + str(attitudes) + "\t" + str(comments) + "\t" + str(action) + "\t" + str(expose) + "\t" + str(
            rate)
        # print(result)
        out.write(result + '\n')
    out.close()


## 获取批量流数据中的各个字段reads,reposts,attitudes,attitudes,comments,action,expose,rate
def get_blog_field_streaming_batch(app_token, mid_path, out_path, n=10):
    # 获取redis
    db_read_0, db_read_1, db_read_2, db_read_3, db_read_4, db_read_5, db_read_6, db_read_7=get_redis()

    # 加载mid
    out = open(out_path, 'w')
    mid_set = set()
    for line in open(mid_path, 'r').readlines():
        mid = line.strip().strip('\n')
        mid_set.add(mid)
    mid_list = list(mid_set)
    mid_size = len(mid_list)

    start = 0
    end = n
    flag = True
    while flag:
        if end >= mid_size:
            end = mid_size
            flag = False

        mid_list_batch = mid_list[start:end]
        blog_information_list = get_like_comments_repost_batch(app_token, mid_list_batch)
        if blog_information_list:
            for item in blog_information_list:
                mid = item[0]
                reads = item[1]
                reposts = item[2]
                attitudes = item[3]
                comments = item[4]
                action, expose, rate = get_act_expose_rate(mid, db_read_0, db_read_1, db_read_2, db_read_3, db_read_4, db_read_5, db_read_6, db_read_7)
                result = str(mid) + '\t' + str(reads) + "\t" + str(reposts) + "\t" \
                         + str(attitudes) + "\t" + str(comments) + "\t" + str(action) + "\t" + str(expose) + "\t" + str(
                    rate)
                # print(result)
                out.write(result + '\n')
        else:
            pass
        start = end
        end = end + n
    out.close()


if __name__ == "__main__":
    # 配置redis
    # h0 = 'rs20218.mars.grid.sina.com.cn'
    # p0 = '20218'
    # db_read_0 = redis.Redis(host=h0, port=p0)
    #
    # h1 = 'rs20373.mars.grid.sina.com.cn'
    # p1 = '20373'
    # db_read_1 = redis.Redis(host=h1, port=p1)
    #
    # h2 = 'rs20374.mars.grid.sina.com.cn'
    # p2 = '20374'
    # db_read_2 = redis.Redis(host=h2, port=p2)
    #
    # h3 = 'rs20375.mars.grid.sina.com.cn'
    # p3 = '20375'
    # db_read_3 = redis.Redis(host=h3, port=p3)
    #
    # h4 = 'rs20376.mars.grid.sina.com.cn'
    # p4 = '20376'
    # db_read_4 = redis.Redis(host=h4, port=p4)
    #
    # h5 = 'rs20377.mars.grid.sina.com.cn'
    # p5 = '20377'
    # db_read_5 = redis.Redis(host=h5, port=p5)
    #
    # h6 = 'rs20378.mars.grid.sina.com.cn'
    # p6 = '20378'
    # db_read_6 = redis.Redis(host=h6, port=p6)
    #
    # h7 = 'rs20379.mars.grid.sina.com.cn'
    # p7 = '20379'
    # db_read_7 = redis.Redis(host=h7, port=p7)

    redis_app_token = redis_token.redisDB(host="rm20435.hebe.grid.sina.com.cn", port=20435,db=3)._Get_token_from_redis()
    print(redis_app_token)

    # base_dir = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/orginal/20170505/'
    # blog_file_name = get_mid_file(base_dir)

    # mid_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/orginal/20170505/' + blog_file_name
    # blog_field_out_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170509/' + blog_file_name + '.blog_field'
    # blog_score_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170509/' + blog_file_name+'.blog_score'
    #
    # get_blog_field_streaming_batch(redis_app_token, mid_path, blog_field_out_path)
    #
    # datas_use, datas_nouse = hot_blog_score.datas_load(blog_field_out_path)
    # datas_min_max = hot_blog_score.datas_min_max_scaler(datas_use)
    # datas_score = hot_blog_score.cal_hot_score(datas_min_max, 0.4, 0.35, 0.05, 0.05, 0.1, 0.05)
    # datas_sort = hot_blog_score.datas_merge_sort(datas_nouse, datas_use, datas_score)
    #
    # hot_blog_score.datas_out(blog_score_path, datas_sort, n=len(datas_sort))

    # print(get_like_comments_repost(redis_app_token, '4110115013338135'))
    print(get_spammer_api('4110189294657937'))
