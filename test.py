# import HKIPcamera
# import time
# import numpy as np
# #import matplotlib.pyplot as plt
# import cv2
#
# ip = str('192.168.33.166')  # 摄像头IP地址，要和本机IP在同一局域网
# name = str('admin')       # 管理员用户名
# pw = str('kunjuee.com')        # 管理员密码
# a = HKIPcamera.init(ip, name, pw)
# print(a != None)
#
# # HKIPcamera.getfram()
# while (a != None):
#     t = time.time()
#     fram = HKIPcamera.getframe()
#     t2 = time.time()
#     cv2.imshow('123', np.array(fram))
#     cv2.waitKey(1)
#     print(t2-t)
#     time.sleep(0.1)
# HKIPcamera.release()

import HKIPcamera

import numpy as np
import cv2

ip = str('192.168.33.214')  # 摄像头IP地址，要和本机IP在同一局域网
name = str('admin')  # 管理员用户名
pw = str('kunjuee.com')  # 管理员密码
def yuv2bgr(y, u, v):
    yuv_img = cv2.merge([y, u, v])
    bgr_img = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR)

    return bgr_img
def bgr2yuv(img):
    yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(yuv_img)

    return y, u, v

HKIPcamera.init(ip, name, pw)
while True:
    fram = HKIPcamera.getframe()

    cv2.namedWindow("frame", 0)  # 0可调大小，注意：窗口名必须imshow里面的一窗口名一直
    cv2.resizeWindow("frame", 1200, 900)
    y, u, v = bgr2yuv(np.array(fram))

    res =yuv2bgr( y, u, v)
    cv2.imwrite("test.jpg",res)
    cv2.imshow('frame', res)

    if cv2.waitKey(24) & 0xff == 27:
        break

HKIPcamera.release()
