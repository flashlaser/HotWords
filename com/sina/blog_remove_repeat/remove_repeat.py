# coding=utf-8

import sys
import extract_words
import shingle_sim

reload(sys)
sys.setdefaultencoding('utf-8')


def remove_repeat_blog(in_path, out_path, similarity_threshold):
    out_file=open(out_path, 'w')

    blog_list=[]
    blog_mid_set=set()
    for line in open(in_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        blog_list.append(items)
    blog_list_size=len(blog_list)
    for i in range(0, blog_list_size):
        one_items=blog_list[i]
        one_blog_mid=one_items[0]
        one_blog_uid=one_items[1]
        one_blog_level=one_items[2]
        one_blog_score=one_items[3]
        one_blog_content_at=one_items[4]
        one_blog_content=one_items[5]
        one_blog_count=one_items[6]
        for j in range(i+1, blog_list_size):
            two_items = blog_list[j]
            two_blog_mid = two_items[0]
            two_blog_uid = two_items[1]
            two_blog_level = two_items[2]
            two_blog_score = two_items[3]
            two_blog_content_at = two_items[4]
            two_blog_content = two_items[5]
            two_blog_count = two_items[6]

            sentence_one=extract_words.filter_symbol(one_blog_content)
            sentence_two=extract_words.filter_symbol(two_blog_content)

            similarity=shingle_sim.shingleSimilarity(sentence_one, sentence_two)
            if similarity > similarity_threshold:
                if one_blog_score > two_blog_score:
                    blog_mid_set.add(one_blog_mid)
                else:
                    blog_mid_set.add(two_blog_mid)
                break
    for mid in blog_mid_set:
        out_file.write(mid+'\n')

    out_file.close()

if __name__=='__main__':
    in_path='/home/littlebei/program/python/pycharm/HotWords/data/blog_remove_repeat/1496826001.blog_contain_hot_words'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/blog_remove_repeat/1496826001.blog_hot'
    remove_repeat_blog(in_path, out_path, 0.6)