# coding=utf-8

from sklearn import preprocessing
import sys
import numpy as np
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')


## 数据加载
def datas_load(file_path):
    datas_use = []  # 用到的数据
    datas_nouse = []  # 没有用到的数据
    for line in open(file_path, 'r').readlines():
        words = line.strip().strip('\n').split('\t')
        # print(len(words))
        tag_name=words[0]
        tag_count=words[1]
        mid = words[2]
        uid = words[3]
        url = words[4]
        level = words[5]
        reads = float(words[6])
        reposts = float(words[7])
        attitudes = float(words[8])
        comments = float(words[9])
        action = float(words[10])
        expose = float(words[11])
        rate = float(words[12])

        data_use = []
        data_nouse = []
        data_nouse.append(tag_name)
        data_nouse.append(tag_count)
        data_nouse.append(mid)
        data_nouse.append(uid)
        data_nouse.append(url)
        data_nouse.append(level)

        data_use.append(reads)
        data_use.append(reposts)
        data_use.append(attitudes)
        data_use.append(comments)
        data_use.append(action)
        data_use.append(expose)
        data_use.append(rate)
        # print(data)
        datas_use.append(data_use)
        datas_nouse.append(data_nouse)
    return datas_use, datas_nouse


## 对数据进行归一化处理
def datas_min_max_scaler(datas):
    datas_array = np.array(datas)
    min_max_scaler = preprocessing.MinMaxScaler()
    datas_min_max = min_max_scaler.fit_transform(datas_array)
    return datas_min_max.tolist()


## 计算每条微博的分数
def cal_hot_score(datas_min_max, reads_weight, reposts_weight, attitudes_weight, comments_weight, action_weight,
                  expose_weight, rate_weight=0):
    datas_score = []
    for data in datas_min_max:
        reads = data[0]
        reposts = data[1]
        attitudes = data[2]
        comments = data[3]
        action = data[4]
        expose = data[5]
        rate = data[6]
        score = reads_weight * reads + reposts_weight * reposts + attitudes_weight * attitudes + comments_weight * comments + action_weight * action + expose_weight * expose + rate * rate_weight

        data.append(score)
        datas_score.append(data)
    return datas_score


## 对没有用到的数据和评分后的数据进行合并和排序（依据分数score进行排序）
def datas_merge_sort(datas_nouse, datas_use, datas_score):
    datas = []
    datas_size = len(datas_score)
    for i in range(0, datas_size):
        tag_name=datas_nouse[i][0]
        tag_count=datas_nouse[i][1]
        mid = datas_nouse[i][2]
        uid = datas_nouse[i][3]
        url = datas_nouse[i][4]
        level = datas_nouse[i][5]

        reads = datas_use[i][0]
        reposts = datas_use[i][1]
        attitudes = datas_use[i][2]
        comments = datas_use[i][3]
        action = datas_use[i][4]
        expose = datas_use[i][5]
        rate = datas_use[i][6]

        score = datas_score[i][7]

        data = []
        data.append(tag_name)
        data.append(tag_count)
        data.append(mid)
        data.append(uid)
        data.append(url)
        data.append(level)
        data.append(reads)
        data.append(reposts)
        data.append(attitudes)
        data.append(comments)
        data.append(action)
        data.append(expose)
        data.append(rate)
        data.append(score)

        datas.append(data)
    # 对合并后的结构进行排序
    datas.sort(key=lambda x: x[13], reverse=True)

    return datas


## 默认返回前20条得分最高的数据
def datas_out(datas_out_path, datas, n=20):
    datas_df = pd.DataFrame(datas)
    datas_n = datas_df.head(n)
    datas_n.to_csv(datas_out_path, index=False, header=False, sep='\t')


if __name__ == '__main__':
    datas_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/20170504_08.blog_filed'
    datas_use, datas_nouse = datas_load(datas_path)
    print(datas_use[0])

    datas_min_max = datas_min_max_scaler(datas_use)
    print(datas_min_max[0])

    datas_score = cal_hot_score(datas_min_max, 0.4, 0.35, 0.05, 0.05, 0.1, 0.05)
    print(datas_score[0])

    datas_sort = datas_merge_sort(datas_nouse, datas_use, datas_score)
    print(len(datas_sort))

    datas_df = pd.DataFrame(datas_sort)
    print(datas_df.head(5))

    datas_out_path = '/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170504/20170504_08.tag_blog_match_score'
    datas_out(datas_out_path, datas_sort, n=len(datas_sort))
