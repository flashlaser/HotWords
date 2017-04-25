# coding=utf-8


def generatorDic(filePath, dicPath):
    try:
        f=open(filePath, 'r')
        dic=open(dicPath, 'w')
        while 1:
            line=f.readline()
            if line:
                words=line.split('\t')
                dic.write(words[0]+'\n')
            else:
                break;
    finally:
        f.close()
        dic.close()


def dealAuthor(targetPath, dicPath, inPath, notInPath, date):
    try:
        dic=open(dicPath, 'r')
        dicList=[]
        while 1:
            line=dic.readline()
            if line:
                words=line.split('\t')
                dicList.append(words[0])
            else:
                break


        target = open(targetPath, 'r')
        authorIn=open(inPath, 'w')
        authorNotIn=open(notInPath, 'w')

        while 1:
            line=target.readline()
            if line:
                words=line.split('\t')
                if words[0]==date:
                    if words[2] in dicList:
                        authorIn.write(words[2]+'\n')
                    else:
                        authorNotIn.write(words[2]+'\n')
                else:
                    pass
            else:
                break
    finally:
        if dic:
            dic.close()
        if target:
            target.close()
        authorIn.close()
        authorNotIn.close()

def dealAuthor(targetPath, dicPath, inPath, notInPath):
    try:
        dic=open(dicPath, 'r')
        dicList=[]
        while 1:
            line=dic.readline()
            if line:
                words=line.split('\t')
                dicList.append(words[4])
            else:
                break


        target = open(targetPath, 'r')
        authorIn=open(inPath, 'w')
        authorNotIn=open(notInPath, 'w')

        while 1:
            line=target.readline()
            if line:
                words=line.split('\n')
                if words[0] in dicList:
                    authorIn.write(words[0]+'\n')
                else:
                    authorNotIn.write(words[0]+'\n')
            else:
                break
    finally:
        if dic:
            dic.close()
        if target:
            target.close()
        authorIn.close()
        authorNotIn.close()


if __name__=='__main__':

    dicPath = '../../../data/author250/Spammer.info_0421'
    targetPath='../../../data/author250/filter_mid.txt'
    inPath='../../../data/author250/in_mid.txt'
    notInPath='../../../data/author250/not_in_mid.txt'
    #path='../../../data/author250/dic.txt'

    #dealAuthor(targetPath, dicPath,inPath, notInPath, '20170328')
    #generatorDic(dicPath, path)
    dealAuthor(targetPath, dicPath, inPath, notInPath)
    print('hi')
