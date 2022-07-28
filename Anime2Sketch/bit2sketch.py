"""Test script for anime-to-sketch translation
Example:
    python3 test.py --dataroot /your_path/dir --load_size 512
    python3 test.py --dataroot /your_path/img.jpg --load_size 512
"""

import os
import torch
from model import create_model
from data import tensor_to_img,img_transform,read_img_path
import cv2


def bit2sketch(img):
    # create model
    gpu_list = ','.join(str(x) for x in [])
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_list
    device = torch.device('cuda' if len([])>0 else 'cpu')
    model = create_model().to(device)      # create a model given opt.model and other options
    model.eval()
    img,  aus_resize = read_img_path('../img/gp.png',0)
    aus_tensor = model(img.to(device))
    aus_img = tensor_to_img(aus_tensor)
    return aus_img

img=cv2.imread('../img/1.jpg',1)
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img=bit2sketch(img)
img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
cv2.imshow('bit2sketch',img)
cv2.waitKey()
