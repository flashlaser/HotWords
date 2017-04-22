# coding=utf-8

## 去除id相同的行，把数据依据ads和badwords分成两部分
def splitSpammer(spammerPath, adsPath, badwordsPath):
    try:
        f=open(spammerPath, 'r')
        ads=open(adsPath, 'w')
        badwords=open(badwordsPath, 'w')
        idList=[]

        while 1:
            line=f.readline()
            words=line.split('\t')
            #print(words[4])
            if line:
                if words[4] in idList:
                    pass
                else:
                    idList.append(words[4])
                    if 'DETECTED ADS' in line:
                        ads.write(line)
                    elif 'TOO MANY BADWORDS' in line:
                        badwords.write(line)
                    else:
                        pass
            else:
                break
    finally:
        f.close()
        ads.close()
        badwords.close()


if __name__=='__main__':
    spammerPath='../../../data/spammer/Spammer.info.5'
    adsPath='../../../data/spammer/Spammer.info.5.ads'
    badwords='../../../data/spammer/Spammer.info.5.badwords'

    splitSpammer(spammerPath, adsPath, badwords)