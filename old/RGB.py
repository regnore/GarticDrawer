from cv2 import sqrt
import numpy as np
import cv2
import json

def colorDistance243(vec1,vec2):
    return 2*pow((vec1[0]-vec2[0]),2)+4*pow((vec1[1]-vec2[1]),2)+3*pow((vec1[2]-vec2[2]),2)
    

with open("json/gartic.json",'r') as load_f:
    colorBtn = json.load(load_f)

'''
for i in range(size):
    for ii in range(i+1,size):
        color.append((np.array(color[i])+np.array(color[ii]))/2)
'''
img = cv2.imread('img/1.jpg', 1)

img = cv2.resize(img, [256,256])


img1=img

i=0
for row in img:
    ii=0
    for p in row:
        temp=999999999
        tempc=[255,255,255]
        for cB in colorBtn:
           # tempcd=colorDistance243([p[2],p[1],p[0]],cB['color'])
            tempcd=np.linalg.norm(np.array([p[2],p[1],p[0]])-np.array(cB['color']))
            if tempcd<=temp:
                tempc=cB['color']
                temp=tempcd
        img1[i][ii]=tempc
        ii=ii+1
    i=i+1

img1=img1.astype('uint8')

img1=cv2.cvtColor(img1,cv2.COLOR_RGB2BGR)
cv2.imshow('OpencvTest', img1)

if cv2.waitKey():
    cv2.destroyAllWindows()