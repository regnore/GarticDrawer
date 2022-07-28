from cv2 import sqrt
import numpy as np
import cv2
import json
import pyautogui
import urllib.request
import mouse
import time

pyautogui.PAUSE = 0.000001
height = 64
interval = 9
tt=0.0001

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    # bytearray将数据转换成（返回）一个新的字节数组
    # asarray 复制数据，将结构化数据转换成ndarray
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image

def draw(imgo,colorBtn):
    times=time.perf_counter()
    mp = pyautogui.position()
    print(mp)
    for i in range(len(colorBtn)):
        if colorBtn[i]['color'][0]!=255 or colorBtn[i]['color'][1]!=255 or colorBtn[i]['color'][2]!=255:
            mouse.move(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1])
            time.sleep(tt)
            mouse.click('left')
            for ii in range(imgo.shape[0]):
                for iii in range(imgo.shape[1]):
                    if imgo[ii][iii][0] == i:
                        mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.click('left')

    mouse.move(con['alphaBtnPosM'][0],con['alphaBtnPosM'][1])
    time.sleep(tt)
    mouse.click('left')

    for i in range(len(colorBtn)):
        mouse.move(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1])
        time.sleep(tt)
        mouse.click('left')
        for ii in range(imgo.shape[0]):
            for iii in range(imgo.shape[1]):
                if imgo[ii][iii][1] == i:
                    mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                    time.sleep(tt)
                    mouse.click('left')

    for i in range(len(colorBtn)):
        mouse.move(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1])
        time.sleep(tt)
        mouse.click('left')
        for ii in range(imgo.shape[0]):
            for iii in range(imgo.shape[1]):
                if imgo[ii][iii][2] == i:
                    mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                    time.sleep(tt)
                    mouse.click('left')
    timee=time.perf_counter()
    print(timee-times)
    

with open("json/garticphone.json", 'r') as load_f:
    con = json.load(load_f)

cM=np.array(con['rgbColors'])

print('Colors ready.Please input url or q to quit')

while (1):
    ip = input()

    if ip != 'q':
        img=cv2.imread('img/6.jpg',1)
        #img = url_to_image(ip)
        imgHeight=img.shape[0]
        imgWidth=img.shape[1]
        width=int(height/imgHeight*imgWidth)
        img = cv2.resize(img, [width, height])
        out=np.zeros([height,width,3])
        for i in range(img.shape[0]):
            for ii in range(img.shape[1]):
                indexR=img[i][ii][2]>>4
                if (img[i][ii][2]-indexR<<4)>=8 and indexR<15:
                    indexR+=1
                indexG=img[i][ii][1]>>4
                if (img[i][ii][1]-indexG<<4)>=8 and indexG<15:
                    indexG+=1
                indexB=img[i][ii][0]>>4
                if (img[i][ii][0]-indexB<<4)>=8 and indexB<15:
                    indexB+=1
                out[i][ii]=cM[indexR][indexG][indexB]
        draw(out,con['colorBtn'])
    if ip == 'q':
        break
