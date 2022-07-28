from cv2 import sqrt
import numpy as np
import cv2
import json
import mouse
import time
import pyautogui
import PIL.ImageGrab
import win32clipboard
import keyboard

pyautogui
filename="json/gartic.json"
height = 64
width=0
interval = 6
tt=0.000001
qFlag=False
dFlag=False

def draw(imgo,colorBtn):
    global qFlag,dFlag
    dFlag=True
    boardW=con['downCornerPos'][0]-con['upCornerPos'][0]
    boardH=con['downCornerPos'][1]-con['upCornerPos'][1]
    mp = (int(boardW/2.0-width*interval/2.0+con['upCornerPos'][0]),int(boardH/2.0-height*interval/2.0+con['upCornerPos'][1]))
    print(mp)
    times=time.perf_counter()
    for i in range(len(colorBtn)):
        if colorBtn[i]['color'][0]!=255 or colorBtn[i]['color'][1]!=255 or colorBtn[i]['color'][2]!=255:
            mouse.move(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1])
            time.sleep(tt)
            mouse.click('left')
            for ii in range(imgo.shape[0]):
                flag=False
                for iii in range(imgo.shape[1]):
                        if qFlag:
                            qFlag=False
                            dFlag=False
                            return
                        if imgo[ii][iii][0] == i and flag==False:
                            mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                            time.sleep(tt)
                            mouse.press('left')
                            flag=True
                        if flag==True and iii+1==width:
                            mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                            time.sleep(tt)
                            mouse.release('left')
                            flag=False
                        if flag==1 and imgo[ii][iii+1][0]!=i:
                            mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                            time.sleep(tt)
                            mouse.release('left')
                            flag=False


    for t in [5,1,4,2,3]:
        x=-(t-1)*abs(con['alphaBtnPos'][0]-con['alphaBtnPos1'][0])/4.0+con['alphaBtnPos1'][0]
        y=-(t-1)*abs(con['alphaBtnPos'][1]-con['alphaBtnPos1'][1])/4.0+con['alphaBtnPos1'][1]
        mouse.move(int(x),int(y))
        print(x,y)
        time.sleep(tt)
        mouse.click('left')
        for i in range(len(colorBtn)):
            mouse.move(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1])
            time.sleep(tt)
            mouse.click('left')
            for ii in range(imgo.shape[0]):
                flag=False
                for iii in range(imgo.shape[1]):
                    if qFlag:
                        qFlag=False
                        dFlag=False
                        return
                    if imgo[ii][iii][1] == i and flag==False and imgo[ii][iii][2]==t:
                        mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.press('left')
                        flag=True
                    if flag==True and iii+1==width:
                        mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.release('left')
                        flag=False
                    if flag==True and imgo[ii][iii+1][1]!=i:
                        mouse.move(mp[0]+iii*interval,mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.release('left')
                        flag=False
                            
    timee=time.perf_counter()
    print(timee-times)
    dFlag=False



def quitDraw():
    global qFlag
    if dFlag:
        print('Quit drawing.')
        qFlag=True

keyboard.add_hotkey('q', quitDraw)

with open(filename, 'r') as load_f:
    con = json.load(load_f)

cM=np.array(con['rgbColors2'])



win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.CloseClipboard()

temp=None

print('Ready.')

while 1:
    qflag=False
    try:
        temp=PIL.ImageGrab.grabclipboard()
    except OSError:
        time.sleep(0.1)
    else:
        time.sleep(0.1)
    if temp is not None:
        print('start.')
        img=np.array(temp)
        img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        #img=cv2.imread('img/6.jpg',1)
        #img = url_to_image(ip)
        imgHeight=img.shape[0]
        imgWidth=img.shape[1]
        width=int(height/imgHeight*imgWidth)
        img = cv2.resize(img, [width, height],interpolation=cv2.INTER_AREA)
        out=np.zeros([height,width,3])
        for i in range(img.shape[0]):
            for ii in range(img.shape[1]):
                indexR=img[i][ii][2]>>4
                if (img[i][ii][2]-indexR<<4)>=8:
                    indexR+=1
                indexG=img[i][ii][1]>>4
                if (img[i][ii][1]-indexG<<4)>=8:
                    indexG+=1
                indexB=img[i][ii][0]>>4
                if (img[i][ii][0]-indexB<<4)>=8:
                    indexB+=1
                out[i][ii]=cM[indexR][indexG][indexB]
        draw(out,con['colorBtn'])
