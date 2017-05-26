# coding:utf-8
import urllib, urllib2
import json
import time
import sys
import redis

reload(sys)
sys.setdefaultencoding('utf-8')


# 获取转评赞
def get_like_comments_repost(mid):
    url = 'http://i2.api.weibo.com/2/statuses/count_sp.json?source=1586188222&ids=' + mid
    jsonstr = urllib2.urlopen(url, timeout=5).read()
    dic = json.loads(jsonstr, strict=False)
    reads = dic[0]['reads']  # 阅读量
    reposts = dic[0]['reposts']  # 转发量
    attitudes = dic[0]['attitudes']  # 点赞数
    comments = dic[0]['comments']  # 评论数
    return (reads, reposts, attitudes, comments)


# 获取互动曝光比
# 参数mid
# 返回值:互动数,曝光数,互动曝光比
def get_act_expose_rate(mid):
    db = None
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
            print e
            continue
    # rate为互动曝光比
    rate = (float(int(action) + 1)) / float((int(expose) + 1))
    return action, expose, rate


if __name__ == "__main__":
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

    outFile = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/20170504_08.blog_filed'
    midFile = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/20170504_08.blog_users_filter'

    out = open(outFile, 'w')

    for line in open(midFile, 'r').readlines():
        line = line.strip().strip('\n')
        # print(line)
        words = line.split('\t')
        tag_name=words[0]
        tag_count=words[1]
        mid = words[2]
        uid = words[3]
        url = words[4]
        level = words[5]
        reads, reposts, attitudes, comments = get_like_comments_repost(mid)
        action, expose, rate = get_act_expose_rate(mid)
        result = tag_name+'\t'+str(tag_count)+'\t'+ mid + "\t" + uid + "\t" + url + "\t" + level + "\t" + str(reads) + "\t" + str(reposts) + "\t" + str(
            attitudes) + "\t" + str(comments) + "\t" + str(action) + "\t" + str(expose) + "\t" + str(rate)
        # print(result)
        out.write(result + '\n')
    out.close()
