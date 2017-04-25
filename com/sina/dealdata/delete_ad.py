# coding=utf-8

## 若文本行中包含广告词则删除该行数据
def deleteAd(readPath, writePath, adPath):
    try:
        f=open(readPath, 'r')
        w=open(writePath, 'w')

        while 1:
            line = f.readline()
            if line:
                if not isContainsAd(line, adPath):
                    w.write(line)
                else:
                    pass
            else:
                break
    finally:
        f.close()
        w.close()

## 检测文本行中是否包含广告词
def isContainsAd(line, adPath):
    try:
        ad = open(adPath, 'r')
        for word in ad:
            if word in line:
                return True
    finally:
        if ad:
            ad.close()
    return False

if __name__=='__main__':
    readPath='../../../data/wbcont.txt.u'
    writePath='../../../data/deal.txt'
    adPath='../../../data/ad.txt'

    deleteAd(readPath, writePath, adPath)
    print('删除广告词完成！')

    # for line in open('../../../data/ad.txt'):
    #     print(line)
    #
    # r=open('../../../data/wbcont.txt.u')
    # for i in range(10):
    #     line=r.readline()
    #     print(line)