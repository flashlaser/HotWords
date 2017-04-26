# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def merge(rFilePath1, rFilePath2, wFilePath):
    blog = {}
    with open(rFilePath1, 'r') as b:
        while True:
            line = b.readline()
            if line:
                line = line.strip().strip('\n')
                words = line.split('\t')
                c_id = words[0]
                url = words[2]
                blog[c_id] = url
            else:
                break
    # for e in blog:
    #     print(e, blog[e])
    print(len(blog))


    wf=open(wFilePath, 'w')
    with open(rFilePath2) as r2:
        while True:
            line=r2.readline()
            if line:
                line=line.strip().strip('\n')
                words=line.split('\t')
                if words[3] in blog:
                    wf.write(words[3]+'\t'+words[4]+'\t'+blog[words[3]]+'\n')
            else:
                break
    wf.close()

if __name__=='__main__':
    filterFile='../../../data/dump'
    blogFile='../../../data/dump'
    usersFile='../../../data/dump'
    outFile='../../../data/dump'

    whiteFilePath='../../../data/users/not_in_white_list_mid.txt'

    dicBlog={}
    for line in open(blogFile, 'r').readlines():
        words=line.strip().strip('\n').split('\t')
        mid=words[0]
        uid=words[1]
        dicBlog[mid]=uid

    dicUsers={}
    for line in open(usersFile, 'r').readlines():
        words=line.strip().strip('\n').split('\t')
        uid=words[0]
        level=words[1]
        dicUsers[uid]=level

    out=open(outFile, 'w')
    for line in open(filterFile, 'r').readlines():
        line=line.strip().strip('\n')
        if line in dicBlog:
            uid=dicBlog[line]
            if uid in dicUsers:
                level=dicUsers[uid]
            else:
                level='C5'
            result=line+'\t'+uid+'\t'+level
            out.write(result+'\n')
        else:
            pass
    out.close()