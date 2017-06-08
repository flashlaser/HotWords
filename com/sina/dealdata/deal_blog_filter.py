# coding=utf-8

import deal_blog_field
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


## 判断一条微博是否为广告
def is_spam(mid):
    spammer_flag = deal_blog_field.get_spammer_api(mid)
    if spammer_flag is None:
        return False
    try:
        spammer_flag_value = int(spammer_flag)
    except:
        spammer_flag_value = 100
    if spammer_flag_value == 100:
        return False
    else:
        return True


## 过滤微博依据广告词
def blog_filter_spam(blog_path, blog_spam_path, blog_no_spam_path):
    blog_spam_file = open(blog_spam_path, 'w')
    blog_no_spam_file = open(blog_no_spam_path, 'w')
    for line in open(blog_path, 'r'):
        line = line.strip().strip('\n')
        items = line.split('\t')
        mid = items[0]
        spam_flag = is_spam(mid)
        if spam_flag:
            blog_spam_file.write(line + '\n')
        else:
            blog_no_spam_file.write(line + '\n')
    blog_spam_file.close()
    blog_no_spam_file.close()


## 过滤微博依据用户等级
def blog_filter_user_level(app_token, users_level_path, blog_path, out_path):
    # 加载过滤用户的字典
    users_level_dic = {}
    for line in open(users_level_path, 'r').readlines():
        line = line.strip().strip('\n')
        items = line.split('\t')
        uid = items[0]
        level = items[1]
        users_level_dic[uid] = level

    # 加载mid
    out = open(out_path, 'w')
    for line in open(blog_path, 'r').readlines():
        line = line.strip().strip('\n')
        items = line.split('\t')
        mid = items[0]
        # reads = items[1]
        # reposts = items[2]
        # attitudes = items[3]
        # comments = items[4]
        # action = items[5]
        # expose = items[6]
        # rate = items[7]
        # score = items[8]

        # 取出blog中的uid, content, created_at, content_length字段
        blog_fields = deal_blog_field.get_uid_level_time_content(app_token, mid)
        if not blog_fields:
            continue
        uid, content, created_at, content_length = blog_fields
        # 过滤用户
        if not uid in users_level_dic:
            continue
        level = users_level_dic[uid]
        result = line + "\t" + str(uid) + "\t" + level + "\t" + created_at + '\t' + content + '\t' + str(content_length)
        out.write(result + '\n')

    out.close()


## 过滤微博依据微博标签
def blog_filter_tag(app_token, tag_path, blog_path, out_path):
    # 加载微博类别黑名单
    tag_black_list = []
    for line in open(tag_path, 'r').readlines():
        tag_id = line.strip().strip('\n')
        tag_black_list.append(tag_id)
        # print(len(tag_black_list))

    # 加载mid
    out = open(out_path, 'w')
    for line in open(blog_path, 'r').readlines():
        line = line.strip().strip('\n')
        items = line.split('\t')
        mid = items[0]

        tag = deal_blog_field.get_tag(app_token, mid)
        if not tag:
            continue
        tag_id, tag_name = tag
        if tag_id in tag_black_list:
            continue
        else:
            out.write(line + '\n')

    out.close()


## 过滤微博依据热词
def blog_filter_hot_words(hot_words_path, in_path, out_path_blog_contain_hot_words,
                          out_path_blog_contain_hot_words_no, hot_word_threshold=2):
    hot_word_list = []
    for word in open(hot_words_path, 'r').readlines():
        word = word.strip().strip('\n')
        hot_word_list.append(word)

    out_file_blog_contain_hot_words = open(out_path_blog_contain_hot_words, 'w')
    out_file_blog_contain_hot_words_no = open(out_path_blog_contain_hot_words_no, 'w')
    for line in open(in_path, 'r').readlines():
        try:
            line = line.strip().strip('\n')
            items = line.split('\t')
            # 取出微博内容字段
            blog_mid = items[0]
            blog_score = items[8]
            blog_uid = items[9]
            blog_level = items[10]
            blog_created_at = items[11]
            blog_content = items[12]

            blog_hot_word_set = set()  # 存放每条微博中包含的热词
            for hot_word in hot_word_list:
                if blog_content.__contains__(hot_word):
                    blog_hot_word_set.add(hot_word)
                else:
                    continue

            count = len(blog_hot_word_set)  # 统计每条微博中包含热词的总数
            result = blog_mid + '\t' + blog_uid + '\t' + blog_level + '\t' + str(
                blog_score) + '\t' + blog_created_at + '\t' + blog_content + '\t' + str(count)
            if count >= hot_word_threshold:
                out_file_blog_contain_hot_words.write(result + '\n')
            else:
                out_file_blog_contain_hot_words_no.write(result + '\n')
        except Exception, e:
            continue

    out_file_blog_contain_hot_words.close()
    out_file_blog_contain_hot_words_no.close()


if __name__ == '__main__':
    # redis_app_token = redis_token.redisDB(host="rm20435.hebe.grid.sina.com.cn", port=20435,db=3)._Get_token_from_redis()
    # users_level_path='/data4/shaojie5/littlebei/data/lib/users_level_filter'
    # tag_path='/data4/shaojie5/littlebei/data/lib/tag_black_id'
    # hot_words_path='/data4/shaojie5/littlebei/data/lib/hot_words.txt'
    # blog_path='/data4/shaojie5/littlebei/data/result/1494599401'
    # blog_filter_users_level_out_path='/data4/shaojie5/littlebei/data/test/1494599401.blog_filter_users_level'
    # blog_filter_tag_out_path='/data4/shaojie5/littlebei/data/test/1494599401.blog_filter_tag'
    # blog_filter_hot_words_out_path='/data4/shaojie5/littlebei/data/test/1494599401.blog_filter_hot_words'
    #
    # blog_filter_user_level(redis_app_token, users_level_path, blog_path, blog_filter_users_level_out_path)
    # blog_filter_tag(redis_app_token, tag_path, blog_filter_users_level_out_path, blog_filter_tag_out_path)
    # blog_filter_hot_words(hot_words_path, blog_filter_tag_out_path, blog_filter_hot_words_out_path, 0)

    # print(is_spam('4110189290209508'))

    blog_path = '/data4/shaojie5/littlebei/data/test/20170522.blog'
    blog_spam_path = '/data4/shaojie5/littlebei/data/test/20170522.blog_spam'
    blog_no_spam_path = '/data4/shaojie5/littlebei/data/test/20170522.blog_no_spam'

    blog_filter_spam(blog_path, blog_spam_path, blog_no_spam_path)
