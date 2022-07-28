import PIL.ImageGrab
import cv2
import numpy as np
import time
import win32clipboard

while(1):
    try:
        temp=PIL.ImageGrab.grabclipboard()
    except OSError:
        time.sleep(0.1)
    else:
        time.sleep(0.1)
    if temp is not None:
        img=np.array(temp)
        img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        cv2.imshow('testPil',img)
        if cv2.waitKey():
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()