from cv2 import sqrt
import numpy as np
import cv2
import json
import pyautogui

pyautogui.PAUSE = 0
width = 64
height = 64
interval = 7


def colorDistance243(vec1, vec2):
    return 2*pow((vec1[0]-vec2[0]), 2)+4*pow((vec1[1]-vec2[1]), 2)+3*pow((vec1[2]-vec2[2]), 2)


def drawscratch(imgo, mP, colorBtn):
    for i in range(len(colorBtn)):
        if colorBtn[i]['color'][0]==0 and colorBtn[i]['color'][1]==0 and colorBtn[i]['color'][2]==0:
            pyautogui.click(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1], button='left')
            pyautogui.click(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1], button='left')
            for ii in range(imgo.shape[0]):
                for iii in range(imgo.shape[1]):
                    if imgo[ii][iii] == i:
                        pyautogui.click(mP[0]+iii*interval,mP[1]+ii*interval, button='left')

def drawcolor(imgo, mP, colorBtn):
    for i in range(len(colorBtn)):
        if colorBtn[i]['color'][0]!=255 or colorBtn[i]['color'][1]!=255 or colorBtn[i]['color'][2]!=255:
                pyautogui.click(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1], button='left')
                pyautogui.click(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1], button='left')
                for ii in range(imgo.shape[0]):
                    for iii in range(imgo.shape[1]):
                        if imgo[ii][iii] == i:
                            pyautogui.click(mP[0]+iii*interval,mP[1]+ii*interval, button='left')



def drawcolora(imgo, mP, colorBtn):
    for i in range(len(colorBtn)):
        pyautogui.click(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1], button='left')
        pyautogui.click(colorBtn[i]['pos'][0],colorBtn[i]['pos'][1], button='left')
        for ii in range(imgo.shape[0]):
            for iii in range(imgo.shape[1]):
                if imgo[ii][iii] == i:
                    pyautogui.click(mP[0]+iii*interval,mP[1]+ii*interval, button='left')


with open("json/garticphone.json", 'r') as load_f:
    colorBtn = json.load(load_f)

size = len(colorBtn)

color = []

for i in range(size):
    tcolor = {}
    tcolor['color1'] = i
    tcolor['color2'] = i
    tcolor['color'] = colorBtn[i]['color']
    color.append(tcolor)

for i in range(size):
    for ii in range(i+1, size):
        tcolor = {}
        tcolor['color1'] = i
        tcolor['color2'] = ii
        tcolor['color'] = (np.array(color[i]['color'])+np.array(color[ii]['color']))/2
        color.append(tcolor)


print('Colors ready.')

while (1):
    ip = input()

    if ip == 's':

        img = cv2.imread('img/1.jpg', 1)

        img = cv2.resize(img, [width, height])

        img1 = img
        imgo1 = np.zeros([height, width], np.uint8)
        imgo2 = np.zeros([height, width], np.uint8)

        i = 0
        for row in img:
            ii = 0
            for p in row:
                temp = pow(2,24)
                tempc = [255, 255, 255]
                tempc = {}
                for c in color:
                   # iii=iii+1
                    # tempcd=colorDistance243([p[2],p[1],p[0]],cB['color'])
                    tempcd = np.linalg.norm(
                        np.array([p[2], p[1], p[0]])-np.array(c['color']))
                    if tempcd <= temp:
                        tempc = c
                        # tempiii=iii
                        temp = tempcd
                #img1[i][ii] = tempc['color']
                imgo1[i][ii] = tempc['color1']
                imgo2[i][ii] = tempc['color2']
                ii = ii+1
            i = i+1

       # img1 = img1.astype('uint8')

        mp = pyautogui.position()
        print(mp)
        drawcolor(imgo1, mp, colorBtn)
        if input()=='d':
            drawcolora(imgo2, mp, colorBtn)
        #img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
        #cv2.imwrite('img/out2.png',img1)
        #cv2.imshow('OpencvTest', img1)
        #cv2.waitKey()

    if ip == 'q':
        cv2.destroyAllWindows()
        break
