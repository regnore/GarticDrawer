from operator import mod
import cv2
import pyautogui
import numpy as np
import json
import mouse
countColor=0

filename="json/gartic.json"
try:
    with open(filename,'r') as load_f:
        con = json.load(load_f)
except:
    con={}

colorBtn=[]
flag=False

mod=0

def MouseEvent(event, x, y, flags, param):
    global countColor,flag
    if event == cv2.EVENT_RBUTTONDOWN:
        if mod==1:
            flag=True
            tposition=pyautogui.position()
            tposition1=mouse.get_position()
            print(tposition,tposition1)
            Btn={}
            Btn['pos']=tposition
            Btn['color']=pyautogui.pixel(tposition.x,tposition.y)
            imgtemp=np.array([[[Btn['color'][2],Btn['color'][1],Btn['color'][0]]]]).astype('uint8')
            labc=cv2.cvtColor(imgtemp,cv2.COLOR_BGR2LAB)[0][0]
            Btn['labColor']=[int(labc[0]/255*100),int(labc[1])-128,int(labc[2])-128]
            colorBtn.append(Btn)
            countColor=countColor+1
            print(countColor,Btn['pos'],Btn['color'],Btn['labColor'])
        if mod==2:
            tposition=pyautogui.position() 
            con['alphaBtnPos']=tposition
            print(tposition)
        if mod==3:
            tposition=pyautogui.position()
            con['upCornerPos']=tposition
            print(tposition)
        if mod==4:
            tposition=pyautogui.position()
            con['downCornerPos']=tposition
            print(tposition)
        if mod==5:
            tposition=pyautogui.position()
            con['alphaBtnPos1']=tposition
            print(tposition)
        if mod==6:
            tposition=pyautogui.position()
            con['sizeBtnPos1']=tposition
            print(tposition)

img = cv2.imread('img/scs.png', 1)
cv2.namedWindow('test', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('test', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback('test', MouseEvent)  # 窗口与回调函数绑定
print('Press num keys to start. (q to quit)')
while True:
    cv2.imshow('test', img)
    temp=cv2.waitKey(1)&0xFF
    if temp == ord('1'): 
        mod=1
        print('Cap color buttons.')
    if temp & 0xFF == ord('2'): 
        mod=2
        print('Cap alpha0.5 position.')
    if temp & 0xFF == ord('3'): 
        mod=3
        print('Cap board upleft corner.')
    if temp & 0xFF == ord('4'): 
        mod=4
        print('Cap board downright corner..')
    if temp & 0xFF == ord('5'): 
        mod=5
        print('Cap alpha0.1 position.')
    if temp & 0xFF == ord('6'): 
        mod=6
        print('Cap size1 position.')
    if temp & 0xFF == ord('q'):  # 摁下q退出
        if flag:
            con['colorBtn']=colorBtn
        with open(filename,"w") as f:
            json.dump(con,f)
            print("File written done.")
        break
cv2.destroyAllWindows()
