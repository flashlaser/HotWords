# coding=utf-8

import sys
import json
import hashlib
import hmac
import hashlib
import urllib2
import urllib, redis
import time
import requests

db = redis.Redis("rm20435.hebe.grid.sina.com.cn", 20435, db="3")
tauth2_token = db.get("tauth2_token_1586188222")


def httpCall(command):
    return commands.getstatusoutput(command)[1]


def hmacSignature(tauth_token_secret, param_str):
    h = hmac.new(tauth_token_secret, param_str, hashlib.sha1)
    s = h.digest()
    return s.encode('base64').rstrip()


def createAuthHeader(token, param, sign):
    m = {'token': token, 'param': param, 'sign': sign}
    arr = urllib.urlencode(m).split('&')
    # authorizationHeader="Authorization:TAuth2 "
    authorizationHeader = "TAuth2 "
    for value in arr:
        pair = value.split("=")
        authorizationHeader += pair[0] + "=\"" + pair[1] + "\","
    return authorizationHeader[0: len(authorizationHeader) - 1]


def get_header():
    global tauth2_token
    global db

    header = ""
    for i in range(3):
        try:
            results = json.loads(tauth2_token.strip('\n').strip('\r'))
            token = results['tauth_token'].encode('utf8')
            token_secert = results['tauth_token_secret'].encode('utf8')
            user = "2768965585"
            sign = hmacSignature(token_secert, "uid=" + user)
            header = createAuthHeader(token, "uid=" + user, sign)
            return header
        except Exception as e:
            tauth2_token = db.get("tauth2_token_1586188222")
            print 'get_header error', e
    return header


def mid_get_coms_3(cids):
    cids = ','.join(cids)
    app_token=' '
    api_url = 'http://i.api.weibo.com/comments/show_batch.json?'
    params = {"source": 3439264077, 'cids': cids, "app_token": app_token}

    for i in xrange(5):
        try:
            req = requests.get(api_url, params=params, timeout=5)
            if not req:
                continue
            print req
            return req
        except Exception, e:
            print('mid_get_coms_2:')
            print(e)
            time.sleep(0.1)
            continue
    return None


def mid_get_coms_2(cids):
    cids = ','.join(cids)
    str='4133710708208344,4133708409646643,4133711580304403,4133711140344379'
    url = 'http://i.api.weibo.com/comments/show_batch.json?source=3439264077&cids=' + cids
    header = get_header()

    for i in xrange(5):
        try:
            req = urllib2.Request(url, None, {"Authorization": header})
            jsonstr = urllib2.urlopen(req, timeout=5).read()
            if not jsonstr:
                continue
            # print jsonstr
            target = json.JSONDecoder().decode(jsonstr)
            targets = []
            if len(target) > 0:
                for item in target:
                    res = item['text']
                    if res == '':
                        continue
                    res = res.encode('utf-8').replace('\n', ' ').replace('\t', ' ')
                    targets.append(res)
            # print targets
            if len(targets) > 0:
                return targets
        except Exception, e:
            print('mid_get_coms_2:')
            print(e)
            time.sleep(0.1)
            continue
    return None


def mid_get_comment(mid, cnt):
    if cnt==0:
        return None
    if cnt>300:
        print('最多只能取三百条')
        return None

    # url = 'http://i2.api.weibo.com/comments/hotflow/score.json?source=1629986123&id=' + mid + '&count=10'
    url = 'http://i2.api.weibo.com/comments/hotflow/score.json?source=1629986123&id=' + mid + '&count=' + '%d' % cnt
    response = ''
    isfail = False
    comment = ''

    for i in range(3):
        if i >= 1 and not isfail: break
        try:
            response = urllib2.urlopen(url)
        except Exception, e:
            # print Exception, ":", e
            print "error happend!!!\t", Exception, ":", e
            isfail = True
            time.sleep(0.01)
            continue
    if i == 3:
        return comment

    ret = response.read()
    target = json.JSONDecoder().decode(ret)
    comment_mids = []
    if target['members'] != []:
        for item in target['members']:
            commid = item['cid']
            if commid != '':
                comment_mids.append(str(commid))
    if len(comment_mids) == 0:
        print mid + '\t comment cid is null'
        return None

    comments_size=len(comment_mids)
    comments=[]
    epoch=comments_size/50
    remainder=comments_size%50
    i=0
    while i<epoch:
        comments.extend(mid_get_coms_2(comment_mids[50*i:50*(i+1)]))
        i+=1
    if remainder!=0:
        comments.extend(mid_get_coms_2(comment_mids[50*i:comments_size-1]))
    return comments


if __name__ == '__main__':
    comments=mid_get_comment('4133392750666962',220)
    print len(comments)
    for item in comments:
        print item

