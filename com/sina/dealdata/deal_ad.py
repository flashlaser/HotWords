# coding=utf-8

## 若文本行中包含广告词则删除该行数据
def ad_filter(in_path, out_path, ad_path):
    # 加载广告词
    ad_list=[]
    for line in open(ad_path, 'r').readlines():
        ad_word=line.strip().strip('\n')
        ad_list.append(ad_word)


    # 去除还有广告词的微博
    out_file=open(out_path, 'w')
    flag=False
    for line in open(in_path, 'r').readlines():
        line=line.strip().strip('\n')
        items=line.split('\t')
        blog_content=items[3]
        for ad in ad_list:
            if ad in blog_content:
                flag=True
                break
        if flag:
            flag=False
            continue
        else:
            out_file.write(line+'\n')
    out_file.close()


if __name__=='__main__':
    readPath='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170515/20170515_11.blog_users'
    writePath='/home/littlebei/program/python/pycharm/HotWords/data/hotming/result/20170515/20170515_11.blog_users_filter_ad'
    adPath='/home/littlebei/program/python/pycharm/HotWords/data/hotming/ad_new.txt'

    ad_filter(readPath, writePath, adPath)
    print('删除广告词完成！')

    # for line in open('../../../data/ad.txt'):
    #     print(line)
    #
    # r=open('../../../data/wbcont.txt.u')
    # for i in range(10):
    #     line=r.readline()
    #     print(line)