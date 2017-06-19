# coding=utf-8

import sys
import pandas as pd
import re
import jieba
import jieba.analyse
import hot_word_score

reload(sys)
sys.setdefaultencoding('utf-8')


## 加载tag字典
def load_tag_category():
    tag_category_path='/data4/shaojie5/littlebei/data/lib/tag_category.info'
    tag_category_dic={}
    for line in open(tag_category_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        tag_id=items[0]
        tag_name=items[1]
        tag_category_dic[tag_id]=tag_name
    return tag_category_dic


## 处理特殊符号
def filter_symbol(context):
    # http正则表达式规则
    re_http = re.compile(r'[a-zA-z]+://[^\s]*')
    # 中英文标点符号正则表达式
    re_punc = re.compile('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*🙄“”《》【】：（）]+'.decode('utf8'))

    context = context.decode('utf-8')
    context = context.strip().strip('\n')
    context = re_http.sub('', context)
    context = re_punc.sub('', context)

    return context


## 合并content
def merge_sentence(content_list):
    sentence = ''
    for content in content_list:
        content=content.strip().strip('\n')
        content=filter_symbol(content)
        sentence=' '.join((sentence, content))
    return sentence


## 获取每条微博得分最高的标签
def filter_blog_by_tag_category_weight(in_path, out_path):
    df_tag=pd.read_table(in_path, names=['mid', 'tag_id', 'tag_name', 'tag_weight'])
    df_tag_top_weight=df_tag.iloc[df_tag.groupby('mid')['tag_weight'].idxmax()]
    df_tag_top_weight.to_csv(out_path, index=False, header=False, sep='\t')


## 合并tag文件和blog文件
def merge_tag_blog(tag_path, blog_path, out_path):
    df_tag=pd.read_table(tag_path, names=['mid', 'tag_id', 'tag_name', 'tag_weight'])
    df_blog=pd.read_table(blog_path, names=['mid', 'content'])
    df_tag_blog=pd.merge(df_tag, df_blog, on='mid')
    df_tag_blog.to_csv(out_path, index=False, header=False, sep='\t')


## 依据tag_id分组，将每组中的content拼接成一句话，然后从中抽取关键词
def tag_keywords_extract_merge(in_path, out_path):
    out_file=open(out_path, 'w')

    df_tag=pd.read_table(in_path, names=['mid', 'tag_id', 'tag_name', 'tag_weight', 'content'])
    df_tag_group=df_tag.groupby('tag_id')
    # 分组抽取关键词
    for tag_id, tag_group in df_tag_group:
        content_list=tag_group['content'].values
        sentence=merge_sentence(content_list)
        # 提取每个tag下的关键词
        key_words = jieba.analyse.extract_tags(sentence, topK=100, withWeight=False)
        if key_words:
            words = ' '.join(key_words)
            result = tag_id + '\t' + words
            out_file.write(result + '\n')
        else:
            continue
    out_file.close()


## 依据tag_id分组，对每组中的每条微博分别抽取关键词
def tag_keywords_extract_single(in_path, out_path):
    tag_category_dic=load_tag_category()
    out_file = open(out_path, 'w')

    df_tag = pd.read_table(in_path, names=['mid', 'tag_id', 'tag_name', 'tag_weight', 'content'])
    df_tag_group = df_tag.groupby('tag_id')
    # 分组抽取关键词
    for tag_id, tag_group in df_tag_group:
        content_list = tag_group['content'].values
        # 提取每个tag下的关键词
        seg_words_list = hot_word_score.jieba_hot_word_tf_idf(content_list)
        key_words=hot_word_score.count_words(seg_words_list)
        top_keywords=hot_word_score.keywords_top(key_words, top_k=200)
        if top_keywords:
            word_list=[]
            for item in top_keywords:
                word=item[0]
                word_count=item[1]
                word_list.append(word+'('+str(word_count)+')')
            words = ' '.join(word_list)
            tag_name=tag_category_dic[tag_id]
            result = tag_id + '\t' + tag_name + '\t' +words
            out_file.write(result + '\n')
        else:
            continue
    out_file.close()



if __name__=='__main__':
    # df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'], 'key2':['one', 'two', 'one', 'two', 'one']})
    # print(df)
    # print(df.values)
    # for item in df.values:
    #     print item[-1]

    # tag_path='/data4/shaojie5/littlebei/data/test/20170522.blog_tag_tagCategory'
    # tag_filter_path='/data4/shaojie5/littlebei/data/test/20170522.blog_tag_tagCategory_top_weight'
    # filter_blog_by_tag_category_weight(tag_path, tag_filter_path)
    #
    # blog_path='/data4/shaojie5/littlebei/data/test/20170522.blog'
    tag_blog_path='/data4/shaojie5/littlebei/data/test/20170522.tag_blog'
    # merge_tag_blog(tag_filter_path, blog_path, tag_blog_path)

    out_path='/data4/shaojie5/littlebei/data/test/20170522.tag_keywords_4'
    # tag_keywords_extract_merge(tag_blog_path, out_path)
    tag_keywords_extract_single(tag_blog_path, out_path)