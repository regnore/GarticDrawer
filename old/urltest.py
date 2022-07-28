import numpy as np
import urllib.request
import cv2
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# URL到图片
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    # bytearray将数据转换成（返回）一个新的字节数组
    # asarray 复制数据，将结构化数据转换成ndarray
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image

# initialize the list of image URLs to download
url=input()

# loop over the image URLs
# download the image URL and display it
image = url_to_image(url)
cv2.imshow('urltest', image)
cv2.waitKey(0)