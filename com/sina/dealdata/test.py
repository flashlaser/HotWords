# coding=utf-8

import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__=='__main__':
    a = "Thu Jun 08 11:53:06 +0800 2017"
    b=time.mktime(time.strptime(a, "%a %b %d %H:%M:%S +0800 %Y"))

    c=time.time()

    print c-b