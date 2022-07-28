import numpy as np
import json

filename="json/garticphone.json"
def colorDistance243(vec1,vec2):
    return 2*pow((vec1[0]-vec2[0]),2)+4*pow((vec1[1]-vec2[1]),2)+3*pow((vec1[2]-vec2[2]),2)
    

with open(filename,'r') as load_f:
    con = json.load(load_f)

colorBtn=con['colorBtn']

color=[]

id=0
for cB in colorBtn:
    tcolor={}
    tcolor['id']=id
    tcolor['color']=cB['color']
    tcolor['color1']=id
    tcolor['color2']=None
    tcolor['color3']=None
    color.append(tcolor)
    id+=1

sizet=len(color)

for i in range(sizet):
    for ii in range(i+1, sizet):
        tcolor = {}
        tcolor['id']=id
        tcolor['color1'] = i
        tcolor['color2'] = ii
        tcolor['color3']=None
        tcolor['color'] = (np.array(color[i]['color'])+np.array(color[ii]['color']))/2
        color.append(tcolor)
        id+=1

sizet1=len(color)

for i in range(sizet):
    for ii in range(i+1, sizet1):
        if color[ii]['color2'] is not None:
            tcolor = {}
            tcolor['id']=id
            tcolor['color1'] = color[ii]['color1']
            tcolor['color2'] = color[ii]['color2']
            tcolor['color3']=i
            tcolor['color'] = (np.array(color[ii]['color'])+np.array(color[i]['color']))/2
            color.append(tcolor)
            id+=1

print('color calculating done.',len(color))

rgbcolors=np.zeros([17,17,17,3])

for i in range(17):
    for ii in range(17):
        for iii in range(17):
            min=pow(2,24)
            minc={}
            for c in color:
                temp=np.linalg.norm(np.array([i<<4 if i<16 else 255,ii<<4 if ii<16 else 255,iii<<4 if iii<16 else 255])-np.array(c['color']))
                if temp<min:
                    min=temp
                    minc=c
            rgbcolors[i][ii][iii][0]=minc['color1']
            rgbcolors[i][ii][iii][1]=minc['color2']
            rgbcolors[i][ii][iii][2]=minc['color3']
    print(i)

print('rgb color matching done.')

con['rgbColors']=rgbcolors.tolist()

print('Tojson done.')

with open(filename,"w") as f:
            json.dump(con,f)
            print("File written done.")