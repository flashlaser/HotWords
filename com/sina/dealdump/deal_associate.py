# coding=utf-8
def findAssociate(filterFilePath, blogFilePath, userFilePath, resultFilePath):

    blog={}
    with open(blogFilePath, 'r') as b:
        while True:
            line=b.readline()
            if line:
                line=line.strip().strip('\n')
                words=line.split('\t')
                c_id=words[0]
                u_id=words[1]
                blog[c_id]=u_id
            else:
                break
    # for e in blog:
    #     print(e, blog[e])
    print(len(blog))

    users={}
    with open(userFilePath, 'r') as u:
        while True:
            line=u.readline()
            if line:
                line=line.strip().strip('\n')
                words=line.split('\t')
                u_id=words[0]
                l_id=words[3]
                users[u_id]=l_id
            else:
                break
    # for e in users:
    #     print(e, users[e])
    print(len(users))

    result=open(resultFilePath, 'w')
    with open(filterFilePath, 'r') as f:
        while True:
            line=f.readline()
            if line:
                line=line.strip().strip('\n')
                if line in blog:
                    u_id=blog[line]
                    if u_id in users:
                        l_id=users[u_id]
                        result.write(line+'\t'+u_id+'\t'+l_id+'\n')
                    else:
                        #print(u_id)
                        result.write(line + '\t' + u_id + '\t' + 'C5' + '\n')
                else:
                    # print(line)
                    pass
            else:
                break
    result.close()

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
    filterFilePath='../../../data/users/filter_mid.txt'
    blogFilePath='../../../data/users/20170421.blog'
    userFilePath='../../../data/users/users_C1-C4_update.update'
    resultFilePath='../../../data/users/result2.txt'

    whiteFilePath='../../../data/users/not_in_white_list_mid.txt'


    # findAssociate(filterFilePath, blogFilePath, userFilePath, resultFilePath)
    merge(blogFilePath, whiteFilePath, resultFilePath)