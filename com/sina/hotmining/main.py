# coding=utf-8

import sys
import redis

from com.sina.hotmining import hot_blog_score
from com.sina.giveme import redis_token
from com.sina.dealdata import deal_blog_field
from com.sina.dealdata import deal_blog_filter
from com.sina.dealdata import deal_blog_sort
from com.sina.dealdata import deal_blog_push

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__=='__main__':
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
    #
    # db_read_7 = redis.Redis(host=h7, port=p7)
    redis_app_token = redis_token.redisDB(host="rm20435.hebe.grid.sina.com.cn", port=20435, db=3)._Get_token_from_redis()

    # base_dir = ''
    # blog_file_name = deal_blog_field.get_mid_file(base_dir)
    print('start------------')
    blog_file_name=''

    mid_path = '/data4/shaojie5/littlebei/data/test/' + blog_file_name
    blog_field_out_path = '/data4/shaojie5/littlebei/data/test/' + blog_file_name + '.blog_field'
    blog_score_path = '/data4/shaojie5/littlebei/data/test/' + blog_file_name + '.blog_score'

    # 获取微博转、评、赞等数量信息
    deal_blog_field.get_blog_field_streaming_batch(redis_app_token, mid_path, blog_field_out_path)

    # 依据转、评、赞等信息计算微博的得分，并依据得分进行排序
    datas_use, datas_nouse = hot_blog_score.datas_load(blog_field_out_path)
    datas_min_max = hot_blog_score.datas_min_max_scaler(datas_use)
    datas_score = hot_blog_score.cal_hot_score(datas_min_max, 0.4, 0.35, 0.05, 0.05, 0.1, 0.05)
    datas_sort = hot_blog_score.datas_merge_sort(datas_nouse, datas_use, datas_score)

    hot_blog_score.datas_out(blog_score_path, datas_sort, n=2000)

    users_level_path = '/data4/shaojie5/littlebei/data/lib/users_level_filter'
    tag_path = '/data4/shaojie5/littlebei/data/lib/tag_black_id'
    hot_words_path = '/data4/shaojie5/littlebei/data/lib/hot_words.txt'

    blog_path = '/data4/shaojie5/littlebei/data/test/'+blog_file_name
    blog_filter_users_level_out_path = '/data4/shaojie5/littlebei/data/test/'+blog_file_name+'.blog_filter_users_level'
    blog_filter_tag_out_path = '/data4/shaojie5/littlebei/data/test/'+blog_file_name+'.blog_filter_tag'
    blog_filter_hot_words_out_path = '/data4/shaojie5/littlebei/data/test/'+blog_file_name+'.blog_filter_hot_words'

    # 依据用户名单进行过滤
    deal_blog_filter.blog_filter_user_level(redis_app_token, users_level_path, blog_path, blog_filter_users_level_out_path)

    # 依据微博标签进行过滤
    deal_blog_filter.blog_filter_tag(redis_app_token, tag_path, blog_filter_users_level_out_path, blog_filter_tag_out_path)

    # 依据微博热词进行过滤
    deal_blog_filter.blog_filter_hot_words(hot_words_path, blog_filter_tag_out_path, blog_filter_hot_words_out_path, 0)

    blog_sort_out_path='/data4/shaojie5/littlebei/data/test/'+blog_file_name+'.blog_sort'
    # 依据每条微博中包含的热词数量进行排序
    deal_blog_sort.sort_hot_words_count(blog_filter_hot_words_out_path, blog_sort_out_path)


    blog_mid_out_path = '/data4/shaojie5/littlebei/data/midfile/mids.txt'

    # 获取微博的mid
    deal_blog_field.get_mid(blog_sort_out_path, blog_mid_out_path)
    # 将微博mid文件推送到展示的服务器上
    deal_blog_push.push_blog_mid_file(blog_mid_out_path)