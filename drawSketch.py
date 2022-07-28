from cv2 import sqrt
import numpy as np
import cv2
import mouse
import time
import json
import pyautogui
import PIL.ImageGrab
import win32clipboard
import keyboard
from data import tensor_to_img, img_transform
import os
import torch
from model import create_model
import random

filename = 'json/gartic.json'
height = 128
width = 0
interval = 4
tt = 0.00001
qFlag = False
dFlag = False


def disorderArray(n):
    a = list(range(n))
    for i in range(n):
        r = int(random.random()*n)
        temp = a[i]
        a[i] = a[r]
        a[r] = temp
    return a


def drawSketch(imgo, colorBtn):
    global qFlag, dFlag, con
    dFlag = True
    boardW = con['downCornerPos'][0]-con['upCornerPos'][0]
    boardH = con['downCornerPos'][1]-con['upCornerPos'][1]
    interval = boardH/height
    mp = (int(boardW/2.0-width*interval/2.0+con['upCornerPos'][0]), int(
        boardH/2.0-height*interval/2.0+con['upCornerPos'][1]))
    print(mp)
    times = time.perf_counter()
    mouse.move(colorBtn[0]['pos'][0], colorBtn[0]['pos'][1])
    time.sleep(tt)
    mouse.click('left')
    for ii in range(imgo.shape[0]):
        flag = False
        for iii in range(imgo.shape[1]):
            if qFlag:
                qFlag = False
                dFlag = False
                return
            if imgo[ii][iii]:
                mouse.move(mp[0]+iii*interval, mp[1]+ii*interval)
                time.sleep(tt)
                mouse.click('left')
    timee = time.perf_counter()
    print(timee-times)
    dFlag = False


def drawSketchLine(q, colorBtn):
    global qFlag, dFlag, con
    dFlag = True
    boardW = con['downCornerPos'][0]-con['upCornerPos'][0]
    boardH = con['downCornerPos'][1]-con['upCornerPos'][1]
    interval = boardH/height
    mp = (int(boardW/2.0-width*interval/2.0+con['upCornerPos'][0]), int(
        boardH/2.0-height*interval/2.0+con['upCornerPos'][1]))
    print(mp)
    times = time.perf_counter()
    mouse.move(colorBtn[0]['pos'][0], colorBtn[0]['pos'][1])
    time.sleep(tt)
    mouse.click('left')
    flagNext = False
    #count=0
    for qP in q:
        if qFlag:
            qFlag = False
            dFlag = False
            return
        if qP == [-1, -1]:
            flagNext = True
        elif qP == [-2, -2]:
            mouse.release('left')
            '''
            if count==20:
                count=0
                r=int(random.random()*18)
                if r==3:
                    r=1
                mouse.move(colorBtn[r]['pos'][0], colorBtn[r]['pos'][1])
                time.sleep(tt)
                mouse.click('left')
            count+=1
            '''
        elif flagNext:
            flagNext = False
            mouse.move(mp[0]+qP[0]*interval, mp[1]+qP[1]*interval)
            time.sleep(tt)
            mouse.press('left')
        else:
            mouse.move(mp[0]+qP[0]*interval, mp[1]+qP[1]*interval)
            time.sleep(tt)
    timee = time.perf_counter()
    print(timee-times)
    dFlag = False


def quitDraw():
    global qFlag
    if dFlag:
        print('Quit drawing.')
        qFlag = True


keyboard.add_hotkey('q', quitDraw)

with open(filename, 'r') as load_f:
    con = json.load(load_f)

win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.CloseClipboard()

gpu_list = ','.join(str(x) for x in [])
os.environ['CUDA_VISIBLE_DEVICES'] = gpu_list
device = torch.device('cuda' if len([]) > 0 else 'cpu')
# create a model given opt.model and other options
model = create_model().to(device)
model.eval()
print()
temp = None
print('Ready.')

while 1:
    qflag = False
    try:
        temp = PIL.ImageGrab.grabclipboard()
    except OSError:
        time.sleep(0.1)
    else:
        time.sleep(0.1)
    if temp is not None:
        print('start.')
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        temp = temp.convert('RGB')
        img, aus_resize = img_transform(temp, 512)
        aus_tensor = model(img.to(device))
        img = tensor_to_img(aus_tensor)
        img = np.array(img)
        width = int(height/aus_resize[1]*aus_resize[0])
        img = cv2.resize(img, [width, height], interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # cv2.imwrite('img/out3.png',img)
        imgo = np.zeros([height, width], dtype='bool')
        for i in range(height):
            for ii in range(width):
                if img[i][ii] < 240:
                    imgo[i][ii] = True
                else:
                    imgo[i][ii] = False
        da = disorderArray(width*height)
        da=list(range(width*height))
        q = []
        for t in da:
            i = int(t/width)
            ii = int(t-i*width)
            if imgo[i][ii]:
                q.append([-1, -1])
                q.append([ii,i])
                IDirect = [1, 0]
                if i != 0 and ii != 0 and i != height-1 and ii != width-1:
                    if imgo[i+1][ii+1]:
                        IDirect = [1, 1]
                    elif imgo[i-1][ii-1]:
                        IDirect = [-1, -1]
                    elif imgo[i-1][ii+1]:
                        IDirect = [1, -1]
                    elif imgo[i+1][ii-1]:
                        IDirect = [-1, 1]
                    elif imgo[i+1][ii]:
                        IDirect = [0, 1]
                    elif imgo[i][ii-1]:
                        IDirect = [-1, 0]
                    elif imgo[i-1][ii]:
                        IDirect = [0, -1]
                    elif imgo[i][ii+1]:
                        IDirect = [1, 0]
                tempx = ii
                tempy = i
                while 1:
                    NDirect=[0,0]
                    imgo[tempy][tempx] = False
                    if tempx == 0 or tempx == width-1 or tempy == 0 or tempy == height-1:
                        q.append([tempx,tempy])
                        break
                    if IDirect == [1, 0]:
                        if imgo[tempy][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy
                            NDirect = [1, 0]
                        elif imgo[tempy+1][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy+1
                            NDirect = [1, 1]
                        elif imgo[tempy-1][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy-1
                            NDirect = [1, -1]
                        else:
                            q.append([tempx,tempy])
                            break
                    elif IDirect == [1, 1]:
                        if imgo[tempy+1][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy+1
                            NDirect = [1, 1]
                        elif imgo[tempy+1][tempx]:
                            tempx = tempx
                            tempy = tempy+1
                            NDirect = [0, 1]
                        elif imgo[tempy][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy
                            NDirect = [1, 0]
                        else:
                            q.append([tempx,tempy])
                            break
                    elif IDirect == [0, 1]:
                        if imgo[tempy+1][tempx]:
                            tempx = tempx
                            tempy = tempy+1
                            NDirect = [0, 1]
                        elif imgo[tempy+1][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy+1
                            NDirect = [-1, 1]
                        elif imgo[tempy+1][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy+1
                            NDirect = [1, 1]
                        else:
                            q.append([tempx,tempy])
                            break
                    elif IDirect == [-1, 1]:
                        if imgo[tempy+1][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy+1
                            NDirect = [-1, 1]
                        elif imgo[tempy][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy
                            NDirect = [-1, 0]
                        elif imgo[tempy+1][tempx]:
                            tempx = tempx
                            tempy = tempy+1
                            NDirect = [0, 1]
                        else:
                            q.append([tempx,tempy])
                            break
                    elif IDirect == [-1, 0]:
                        if imgo[tempy][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy
                            NDirect = [-1, 0]
                        elif imgo[tempy-1][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy-1
                            NDirect = [-1, -1]
                        elif imgo[tempy+1][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy+1
                            NDirect = [-1, 1]
                        else:
                            q.append([tempx,tempy])
                            break
                    elif IDirect == [-1, -1]:
                        if imgo[tempy-1][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy-1
                            NDirect = [-1, -1]
                        elif imgo[tempy-1][tempx]:
                            tempx = tempx
                            tempy = tempy-1
                            NDirect = [0, -1]
                        elif imgo[tempy][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy
                            NDirect = [-1, 0]
                        else:
                            q.append([tempx,tempy])
                            break
                    elif IDirect == [0, -1]:
                        if imgo[tempy-1][tempx]:
                            tempx = tempx
                            tempy = tempy-1
                            NDirect = [0, -1]
                        elif imgo[tempy-1][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy-1
                            NDirect = [1, -1]
                        elif imgo[tempy-1][tempx-1]:
                            tempx = tempx-1
                            tempy = tempy-1
                            NDirect = [-1, -1]
                        else:
                            q.append([tempx,tempy])
                            break
                    elif IDirect == [1, -1]:
                        if imgo[tempy-1][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy-1
                            NDirect = [1, -1]
                        elif imgo[tempy][tempx+1]:
                            tempx = tempx+1
                            tempy = tempy
                            NDirect = [1, 0]
                        elif imgo[tempy-1][tempx]:
                            tempx = tempx
                            tempy = tempy-1
                            NDirect = [0, -1]
                        else:
                            q.append([tempx,tempy])
                            break
                    if NDirect!=IDirect:
                        q.append([tempx-NDirect[0],tempy-NDirect[1]])
                        IDirect=NDirect
                q.append([-2, -2])
        # drawSketch(imgo,con['colorBtn'])
        print(len(q))
        drawSketchLine(q, con['colorBtn'])
