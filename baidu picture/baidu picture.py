# -*- coding:utf-8 -*-

import requests
import re
import threading
import urllib
import os
def get_img():
    imglist=[]
    url = 'https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%CE%DE%B5%D0%C6%C6%BB%B5%CD%F5&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=111111'
    r = requests.get(url)
    ptn = re.compile('"hoverURL":"(.*?)"')
    imglist=ptn.findall(r.content)
    return imglist
gimglist = []
i=0
gcondition = threading.Condition()
class Producer(threading.Thread):
    def run(self):
        global gimglist
        global gcondition
        # global i
        gcondition.acquire()
        imglist=get_img()
        print imglist
        for i in imglist:
            gimglist.append(i)
        gcondition.notify_all()
        gcondition.release()

class Consumer(threading.Thread):
    def run(self):
        while True:
            global gimglist
            global gcondition
            global i
            gcondition.acquire()
            while len(gimglist)==0:
                gcondition.wait()
            url=gimglist.pop()
            i = i+1
            print i
            gcondition.release()
            print url
            url = url.replace('\/', '/')
            print url
            img_download(url,i)

def img_download(url,index):

    path='C:/Users/surongling/Desktop/无敌破坏王/无敌破坏王%d.jpg'%index
    path=unicode(path,'utf-8')
    r=requests.get(url)
    with open(path,'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    Producer().start()
    for i in range(1):
        Consumer().start()




