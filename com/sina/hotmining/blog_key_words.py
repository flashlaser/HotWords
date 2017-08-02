# coding=utf-8

import sys
import jieba
import jieba.analyse
import re
from com.sina.dealdata import deal_blog_comment
from com.sina.dealdata import deal_blog_field
from com.sina.giveme import redis_token

reload(sys)
sys.setdefaultencoding('utf-8')


## 处理特殊符号
def filter_symbol(context):
    re_emotion = re.compile(r'\[(.*?)\]')
    # http正则表达式规则
    re_http = re.compile(r'[a-zA-z]+://[^\s]*')
    # 中英文标点符号正则表达式
    re_punc = re.compile(r'[\s+\.\!\/_,$%^*(+\"\'\]+|\[+——！，。？、~@#￥%……&*🙄“”《》【】：（）]+')

    context = context.decode('utf-8')
    # print context
    context = context.strip().strip('\n')
    context = re_http.sub('', context)
    context = re_emotion.sub('', context)
    context = re_punc.sub('', context)
    # print context
    return context

def filter_blog(comments):
    comment_list=[]
    for comment in comments:
        comment_list.append(filter_symbol(comment))
    return ','.join(comment_list)


def get_blog_keywords(app_token, mid):
    blog_field = deal_blog_field.get_uid_level_time_content(app_token, mid)
    if blog_field:
        content=blog_field[1]
        comment_list = deal_blog_comment.mid_get_comment(mid, 300)
        comments = filter_blog(comment_list)
        # 'ns', 'n', 'vn', 'v'
        key_words_tfidf = jieba.analyse.extract_tags(comments, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
        key_words_textrank = jieba.analyse.textrank(comments, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
        return content, ' '.join(key_words_tfidf), ' '.join(key_words_textrank)
    return None


def get_blogs_keywords(app_token, mids_path):
    for line in open(mids_path, 'r').readlines():
        mid=line.strip().strip('\n')
        items=get_blog_keywords(app_token, mid)
        if items:
            print items[0]
            print items[1]
            print items[2]
        else:
            continue


if __name__=='__main__':
    redis_app_token = redis_token.redisDB(host="rm20435.hebe.grid.sina.com.cn", port=20435,
                                          db=3)._Get_token_from_redis()
    # print deal_blog_field.get_uid_level_time_content(redis_app_token, '4133392750666962')
    #
    # comment_list=deal_blog_comment.mid_get_comment('4133392750666962', 300)
    # comments=filter_blog(comment_list)
    # # 'ns', 'n', 'vn', 'v'
    # key_words=jieba.analyse.extract_tags(comments, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
    # for item in key_words:
    #     print item
    #
    # print('----------------------------------------')
    # key_words = jieba.analyse.textrank(comments, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
    # for item in key_words:
    #     print item
    mids_path='/data4/shaojie5/littlebei/project/python/BlogKeywords/mids.txt'
    get_blogs_keywords(redis_app_token, mids_path)