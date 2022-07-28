import numpy as np
import json

filename="json/gartic.json"

with open(filename,'r') as load_f:
    con = json.load(load_f)

def colorDistance(c1,c2):
    ra=(c1[0]+c2[0])/2.0
    dr=c1[0]-c2[0]
    dg=c1[1]-c2[1]
    db=c1[2]-c2[2]
    return (2+ra/256)*dr*dr+4*dg*dg+(2+(255-ra)/256)*db*db

colorBtn=con['colorBtn']

color=[]

id=0
for cB in colorBtn:
    tcolor={}
    tcolor['id']=id
    tcolor['color']=cB['color']
    tcolor['color1']=id
    tcolor['color2']=None
    tcolor['alpha']=0
    color.append(tcolor)
    id+=1

sizet=len(color)

for i in range(sizet):
    for ii in range(i+1, sizet):
        for iii in range(6):
            tcolor = {}
            tcolor['id']=id
            tcolor['color1'] = i
            tcolor['color2'] = ii
            tcolor['alpha']=iii
            tcolor['color'] = np.array(color[i]['color'])*(1-tcolor['alpha']*0.1)+np.array(color[ii]['color'])*tcolor['alpha']*0.1
            color.append(tcolor)
            id+=1

print('color calculating done.',len(color))

rgbcolors=np.zeros([17,17,17,3])
t=pow(2,24)
for i in range(17):
    for ii in range(17):
        for iii in range(17):
            min=t
            minc={}
            for c in color:
                temp=colorDistance(np.array([i<<4 if i<16 else 255,ii<<4 if ii<16 else 255,iii<<4 if iii<16 else 255]),np.array(c['color']))
                if temp<min:
                    min=temp
                    minc=c
            rgbcolors[i][ii][iii][0]=minc['color1']
            rgbcolors[i][ii][iii][1]=minc['color2']
            rgbcolors[i][ii][iii][2]=minc['alpha']
    print(i)

print('rgb color matching done.')

con['rgbColors2']=rgbcolors.tolist()

print('Tojson done.')

with open(filename,"w") as f:
            json.dump(con,f)
            print("File written done.")