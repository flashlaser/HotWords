# coding=utf-8
def splitWbcont(filePath, splitPath, fileRows, n):
    try:
        blockSize=fileRows/n+1
        print(blockSize)

        f = open(filePath)
        for i in range(n):
            s=open(splitPath+'wbcont_'+str(i)+'.txt', 'w')
            for j in range(blockSize):
                line=f.readline()
                #print(line)
                if line:
                    s.write(line)
                else:
                    return
    finally:
        if f:
            f.close()


if __name__=='__main__':
    wbcontPath='../../../data/wbcont/wbcont.txt.u'
    splitPath='../../../data/wbcont/'
    splitWbcont(wbcontPath, splitPath, 3368036, 60)