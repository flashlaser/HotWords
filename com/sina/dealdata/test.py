# coding=utf-8

def splitSpammer(filePath):
    f=open(filePath, 'r')
    list=[]
    for i in range(10):
        line=f.readline()
        words=line.split('\t')
        print(line)
        print(words[0])

if __name__=='__main__':
    print('hello')
    filePath='../../../data/author250/all_28.txt'
    splitSpammer(filePath)
    print('test')