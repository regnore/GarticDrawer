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
from data import tensor_to_img, img_transform
import os
import torch
from model import create_model
import random

filename = "json/gartic.json"
cheight = 64
cwidth = 0
sheight = 128
swidth = 0
tt = 0.005
qFlag = False
dFlag = False
con = {}


def drawSketchLine(q):
    times = time.perf_counter()
    global qFlag, dFlag, con
    colorBtn = con['colorBtn']
    dFlag = True
    boardW = con['downCornerPos'][0]-con['upCornerPos'][0]
    boardH = con['downCornerPos'][1]-con['upCornerPos'][1]
    interval = boardH/sheight
    mp = (int(boardW/2.0-swidth*interval/2.0+con['upCornerPos'][0]), int(boardH/2.0-sheight*interval/2.0+con['upCornerPos'][1]))
    print(mp)
    mouse.move(colorBtn[0]['pos'][0], colorBtn[0]['pos'][1])
    time.sleep(tt)
    mouse.click('left')
    mouse.move(con['sizeBtnPos1'][0],con['sizeBtnPos1'][1])
    time.sleep(tt)
    mouse.click('left')
    pyautogui.press('up',presses=1)
    mouse.move(int(2*con['alphaBtnPos'][0]-con['alphaBtnPos1'][0]),int(2*con['alphaBtnPos'][1]-con['alphaBtnPos1'][1]))
    time.sleep(tt)
    mouse.click('left')
    flagNext = False
    # count = 0
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
            if count == 20:
                count = 0
                r = int(random.random()*18)
                if r == 3:
                    r = 1
                mouse.move(colorBtn[r]['pos'][0], colorBtn[r]['pos'][1])
                time.sleep(tt)
                mouse.click('left')
            count += 1
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
    print('Draw skecth time:',timee-times)
    dFlag = False


def drawColor(imgo):
    times=time.perf_counter()
    global qFlag, dFlag, con, cwidth
    colorBtn = con['colorBtn']
    dFlag = True
    boardW = con['downCornerPos'][0]-con['upCornerPos'][0]
    boardH = con['downCornerPos'][1]-con['upCornerPos'][1]
    interval = boardH/cheight
    mp = (int(boardW/2.0-cwidth*interval/2.0+con['upCornerPos'][0]), int(
        boardH/2.0-cheight*interval/2.0+con['upCornerPos'][1]))
    print(mp, cwidth)
    mouse.move(con['sizeBtnPos1'][0],con['sizeBtnPos1'][1])
    time.sleep(tt)
    mouse.click('left')
    pyautogui.press('up',presses=int(interval/3.0*2.0))
    for i in range(len(colorBtn)):
        if colorBtn[i]['color'][0] != 255 or colorBtn[i]['color'][1] != 255 or colorBtn[i]['color'][2] != 255:
            mouse.move(colorBtn[i]['pos'][0], colorBtn[i]['pos'][1])
            time.sleep(tt)
            mouse.click('left')
            for ii in range(imgo.shape[0]):
                flag = False
                for iii in range(imgo.shape[1]):
                    if qFlag:
                        qFlag = False
                        dFlag = False
                        return
                    if imgo[ii][iii][0] == i and flag == False:
                        mouse.move(mp[0]+iii*interval, mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.press('left')
                        flag = True
                    if flag == True and iii+1 == cwidth:
                        mouse.move(mp[0]+iii*interval, mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.release('left')
                        flag = False
                    if flag == 1 and imgo[ii][iii+1][0] != i:
                        mouse.move(mp[0]+iii*interval, mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.release('left')
                        flag = False

    for t in [5, 1, 4, 2, 3]:
        mouse.move( con['alphaBtnPos'][0], con['alphaBtnPos'][1])
        time.sleep(tt)
        mouse.click('left')
        pyautogui.press('down',presses=5-t)
        for i in range(len(colorBtn)):
            mouse.move(colorBtn[i]['pos'][0], colorBtn[i]['pos'][1])
            time.sleep(tt)
            mouse.click('left')
            for ii in range(imgo.shape[0]):
                flag = False
                for iii in range(imgo.shape[1]):
                    if qFlag:
                        qFlag = False
                        dFlag = False
                        return
                    if imgo[ii][iii][1] == i and flag == False and imgo[ii][iii][2] == t:
                        mouse.move(mp[0]+iii*interval, mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.press('left')
                        flag = True
                    if flag == True and iii+1 == cwidth:
                        mouse.move(mp[0]+iii*interval, mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.release('left')
                        flag = False
                    if flag == True and imgo[ii][iii+1][1] != i:
                        mouse.move(mp[0]+iii*interval, mp[1]+ii*interval)
                        time.sleep(tt)
                        mouse.release('left')
                        flag = False
    dFlag = False
    timee = time.perf_counter()
    print('Draw color time:',timee-times)

def quitDraw():
    global qFlag
    if dFlag:
        print('Quit drawing.')
        qFlag = True


def calColor(temp):
    global cwidth, cheight
    img = np.array(temp)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    cwidth = int(cheight/imgHeight*imgWidth)
    img = cv2.resize(img, [cwidth, cheight], interpolation=cv2.INTER_AREA)
    out = np.zeros([cheight, cwidth, 3])
    for i in range(img.shape[0]):
        for ii in range(img.shape[1]):
            indexR = img[i][ii][2] >> 4
            indexG = img[i][ii][1] >> 4
            indexB = img[i][ii][0] >> 4
            if (img[i][ii][2]-indexR << 4) >= 8:
                indexR += 1
                indexG = img[i][ii][1] >> 4
            if (img[i][ii][1]-indexG << 4) >= 8:
                indexG += 1
                indexB = img[i][ii][0] >> 4
            if (img[i][ii][0]-indexB << 4) >= 8:
                indexB += 1
            out[i][ii] = cM[indexR][indexG][indexB]
    return out


def calSketch(temp):
    global swidth, sheight, model
    temp = temp.convert('RGB')
    img, aus_resize = img_transform(temp, 512)
    aus_tensor = model(img.to(device))
    img = tensor_to_img(aus_tensor)
    img = np.array(img)
    swidth = int(sheight/aus_resize[1]*aus_resize[0])
    img = cv2.resize(img, [swidth, sheight], interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgo = np.zeros([sheight, swidth], dtype='bool')
    for i in range(sheight):
        for ii in range(swidth):
            if img[i][ii] < 240:
                imgo[i][ii] = True
            else:
                imgo[i][ii] = False
    #da = disorderArray(width*height)
    da = list(range(swidth*sheight))
    q = []
    for t in da:
        i = int(t/swidth)
        ii = int(t-i*swidth)
        if imgo[i][ii]:
            q.append([-1, -1])
            q.append([ii, i])
            IDirect = [1, 0]
            if i != 0 and ii != 0 and i != sheight-1 and ii != swidth-1:
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
                NDirect = [0, 0]
                imgo[tempy][tempx] = False
                if tempx == 0 or tempx == swidth-1 or tempy == 0 or tempy == sheight-1:
                    q.append([tempx, tempy])
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
                        q.append([tempx, tempy])
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
                        q.append([tempx, tempy])
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
                        q.append([tempx, tempy])
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
                        q.append([tempx, tempy])
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
                        q.append([tempx, tempy])
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
                        q.append([tempx, tempy])
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
                        q.append([tempx, tempy])
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
                        q.append([tempx, tempy])
                        break
                if NDirect != IDirect:
                    q.append([tempx-NDirect[0], tempy-NDirect[1]])
                    IDirect = NDirect
            q.append([-2, -2])
    return q


keyboard.add_hotkey('q', quitDraw)

with open(filename, 'r') as load_f:
    con = json.load(load_f)

cM = np.array(con['rgbColors2'])

gpu_list = ','.join(str(x) for x in [])
os.environ['CUDA_VISIBLE_DEVICES'] = gpu_list
device = torch.device('cuda' if len([]) > 0 else 'cpu')
model = create_model().to(device)
model.eval()
temp = None

win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.CloseClipboard()

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
        cout = calColor(temp)
        sout = calSketch(temp)
        drawColor(cout)
        # drawSketch(imgo,con['colorBtn'])
        drawSketchLine(sout)
