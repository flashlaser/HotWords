# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def tag_match_blog(tag_path, blog_path, out_path):
    out_file = open(out_path, 'w')
    for line in open(tag_path, 'r').readlines():
        line = line.strip().strip('\n')
        tag = line.split('\t')
        tag_name = tag[0]
        tag_words = tag[1].split('\001')
        tag_count = tag[2]
        for line in open(blog_path, 'r').readlines():
            line = line.strip().strip('\n')
            blog = line.split('\t')
            mid = blog[0]
            uid = blog[1]
            url = blog[2]
            content = blog[3]
            count = 0  # 统计话题标签中匹配到的词的个数
            for word in tag_words:
                if content.__contains__(word):
                    count = count + 1
                else:
                    pass
            if count == 0:
                continue
            # 拼接输出文本
            result = tag_name + '\t' + str(tag_count) + '\t' + str(mid) + '\t' + str(uid) + '\t' + url
            if content.__contains__(tag_name):
                out_file.write(result + '\n')
            elif len(tag_words) == 2 and count == 2:
                out_file.write(result + '\n')
            elif len(tag_words) == 3 and count == 3:
                out_file.write(result + '\n')
            elif len(tag_words) == 4 and count == 4:
                out_file.write(result + '\n')
            elif len(tag_words) == 5 and count >= 4:
                out_file.write(result + '\n')
            elif len(tag_words) == 6 and count >= 5:
                out_file.write(result + '\n')
            elif len(tag_words) >= 7 and count >= 6:
                out_file.write(result + '\n')
            else:
                continue
    out_file.close()


if __name__=='__main__':
    tag_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/tag_sort_20170504_08_filter_seg.txt'
    blog_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/orginal/20170504/20170504_08.blog'
    out_path='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/tag_match_blog_20170504_08.txt'

    tag_match_blog(tag_path, blog_path, out_path)