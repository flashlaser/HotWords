# coding=utf-8

import sys
import extract_words
import jaccard_sim

reload(sys)
sys.setdefaultencoding('utf-8')


def remove_repeat_blog(in_path, out_path, similarity_threshold, hot_blog_num):
    out_file=open(out_path, 'w')

    blog_list=[]
    for line in open(in_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        blog_list.append(items)

    blog_mid_list = []
    blog_cluster = []

    for i in range(0, len(blog_list)):
        similarity_list = []
        one_items=blog_list[i]
        one_blog_mid=one_items[0]
        one_blog_content=one_items[5]
        if one_blog_mid in blog_mid_list:
            continue
        else:
            similarity_list.append(one_items)
            blog_mid_list.append(one_blog_mid)

        for j in range(i+1, len(blog_list)):
            two_items = blog_list[j]
            two_blog_mid = two_items[0]
            two_blog_content = two_items[5]

            if two_blog_mid in blog_mid_list:
                continue
            else:
                one_sentence=extract_words.filter_symbol(one_blog_content)
                one_sentence=extract_words.extract_keywords_tf_idf(one_sentence, 10)

                two_sentence=extract_words.filter_symbol(two_blog_content)
                two_sentence=extract_words.extract_keywords_tf_idf(two_sentence, 10)

                similarity=jaccard_sim.cal_similarity(one_sentence, two_sentence)

                if similarity > similarity_threshold:
                    similarity_list.append(two_items)
                    blog_mid_list.append(two_blog_mid)

        blog_cluster_item=[]
        blog_cluster_item.append(similarity_list)
        blog_cluster_item.append(len(similarity_list))
        blog_cluster.append(blog_cluster_item)

    for cluster in blog_cluster:
        if len(cluster[0])>1:
            hot_blog_list=cluster[0][0:hot_blog_num]
        else:
            hot_blog_list=cluster[0]

        for blog in hot_blog_list:
            result = '\t'.join(blog)
            out_file.write(result + '\n')
    out_file.close()


if __name__=='__main__':
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/blog_remove_repeat/1496826001.blog_contain_hot_words'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/blog_remove_repeat/1496826001.blog_hot'
    blog_cluster=remove_repeat_blog(in_path, out_path, 0.25, 2)
    print 'end'

    # one_sentence = '#晓说2017#节目神预测！高晓松押中高考题，从预测奥斯卡到预测#高考作文#，江苏高考见证新一代预测帝诞生！说到古今中外未来出行，我只服@高晓松 ，到底矮大紧咋说的？不废话看视频[笑而不语]http://t.cn/Ra1nDIH '
    # one_sentence = extract_words.filter_symbol(one_sentence)
    # one_sentence=extract_words.extract_keywords_tf_idf(one_sentence, 10)
    # print one_sentence
    #
    # two_sentence = '高晓松押中高考题，就是不知道这一年压了多少个考题。女子面试自称有颜值有气质，哎，狗生如戏，全靠演技，我可能遇到了一只假狗[摊手]#分享南京# http://t.cn/RMFrrlN ​'
    # two_sentence = extract_words.filter_symbol(two_sentence)
    # two_sentence=extract_words.extract_keywords_tf_idf(two_sentence, 10)
    # print two_sentence
    #
    # similarity=jaccard_sim.cal_similarity(one_sentence, two_sentence)
    # print similarity