# coding=utf-8
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

## 获取字符串中警号之间的内容
def getSirenContent(filePath):
    pattern=re.compile('#(.*?)#')

    with open(filePath, 'r') as f:
        while True:
            line=f.readline()
            if line:
                contentList=pattern.findall(line)
                if contentList:
                    for c in contentList:
                        print(c)
            else:
                break

if __name__=='__main__':
    filePath='../../../data/test.txt'
    getSirenContent(filePath)
    print('你好')