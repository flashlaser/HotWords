# coding=utf-8
import sys
import jieba
import re

## 设置系统编码
reload(sys)
sys.setdefaultencoding('utf-8')

## 去除文本中无关内容
def delNoText(rFilePath, wFilePath):
    # 匹配http链接规则
    patternHttp=re.compile(r'http://[\S]+')
    # 匹配qq规则
    patternQQ=re.compile(r'[QQ|qq]+[:|：|\s]*\d{6,10}')
    # 匹配数字规则
    patternNum=re.compile(r'\d+\.*\d+')
    # 匹配字母规则
    patterLetter=re.compile(r'\w+')

    wf=open(wFilePath, 'w')
    with open(rFilePath, 'r') as rf:
        while True:
            line=rf.readline()
            if line:
                #line=line.strip() # 去除文本行中的头尾空格
                line=patternHttp.sub('', line) # 去除文本行中的http链接
                line=patternQQ.sub('', line) # 去除文本行中的qq号
                line=patternNum.sub('', line)  # 去除文本行中的数字
                line=patterLetter.sub('', line) # 去除文本行中的字母
                wf.write(line)
            else:
                break;
    wf.close()

## 对文本进行分词
def splitWord(stopwordsPath, rFilePath, wFilePath):
    # 加载停用词表
    stopwords=[]
    with open(stopwordsPath, 'r') as sw:
        while True:
            line=sw.readline()
            if line:
                words=line.split('\n')
                stopwords.append(words[0])
            else:
                break

    # 加载分词后要写入的文件
    wf=open(wFilePath, 'w')

    # 加载要分词的文件
    with open(rFilePath, 'r') as rf:
        while True:
            line=rf.readline()
            if line:
                str=line.strip().strip('\n') # 去除文本行中的空格和换行符
                segList=jieba.cut(str, cut_all=False)
                outList=[]
                for w in list(segList):
                    if w in stopwords:
                        pass
                    else:
                        outList.append(w)
                output=' '.join(outList)
                wf.write(output+'\n')
            else:
                break
    wf.close()


if __name__=='__main__':
    # 存放停用词的路径
    stopwordsPath='../../../data/word2vec/stop_words_1893.txt'
    # 读取要处理的文本
    rFilePath='../../../data/word2vec/country.txt'
    # 文本预处理后存放路径
    pFilePath='../../../data/word2vec/pre.txt'
    # 存放分词后的文本路径
    splitPath='../../../data/word2vec/result.txt'


    delNoText(rFilePath, pFilePath)
    splitWord(stopwordsPath, pFilePath, splitPath)