from arcface.engine import *
import HKIPcamera

import numpy as np
import cv2

#摄像头视频的帧率正常在25~30帧左右，并且一般的视频帧的分辨率为1280x720，当然有的摄像头可以达到更大的分辨率，12080*720效果最好，不卡

APPID = b'8j3iL2sTNbZkiZKKbeWGeWmt2HFNujU9wyegjHVRD49f'
SDKKey = b'31HA4YZZVFtQMQ2qTEM6DPduBYLA2vXAh5KxtgU3oDK2'
# 激活接口,首次需联网激活
res = ASFOnlineActivation(APPID, SDKKey)
if (MOK != res and MERR_ASF_ALREADY_ACTIVATED != res):
    print("ASFActivation fail: {}".format(res))
else:
    print("ASFActivation sucess: {}".format(res))

# 获取激活文件信息
res, activeFileInfo = ASFGetActiveFileInfo()

if (res != MOK):
    print("ASFGetActiveFileInfo fail: {}".format(res))
else:
    print(activeFileInfo)

# 获取人脸识别引擎
face_engine = ArcFace()

# 需要引擎开启的功能
mask = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS | ASF_IR_LIVENESS

# 初始化接口
res = face_engine.ASFInitEngine(ASF_DETECT_MODE_IMAGE, ASF_OP_0_ONLY, 30, 10, mask)
if (res != MOK):
    print("ASFInitEngine fail: {}".format(res))
else:
    print("ASFInitEngine sucess: {}".format(res))

ip = str('192.168.33.214')  # 摄像头IP地址，要和本机IP在同一局域网
name = str('admin')  # 管理员用户名
pw = str('kunjuee.com')  # 管理员密码
# RGB图像
img1 = cv2.imread("asserts/1.jpg")
img2 = cv2.imread("asserts/2.jpg")
# IR活体检测图像
img3 = cv2.imread("asserts/3.jpg")
img4 = cv2.imread("asserts/4.jpg")
img5 = cv2.imread("asserts/5.jpg")
img6 = cv2.imread("asserts/6.jpg")
img7 = cv2.imread("asserts/7.jpg")
HKIPcamera.init(ip, name, pw)
while True:
    fram = HKIPcamera.getframe()

    cv2.namedWindow("frame", 0)  # 0可调大小，注意：窗口名必须imshow里面的一窗口名一直
    cv2.resizeWindow("frame", 600, 400)
    # y, u, v = bgr2yuv(np.array(fram))
    #
    # res =yuv2bgr( y, u, v)
    cv2.imshow('frame', np.array(fram))

    #     if cv2.waitKey(24) & 0xff == 27:
    #         break
    #
    # HKIPcamera.release()

    # # RGB图像
    # img1 = cv2.imread("asserts/1.jpg")
    # img2 = cv2.imread("asserts/2.jpg")
    # # IR活体检测图像
    # img3 = cv2.imread("asserts/3.jpg")
    # img4 = cv2.imread("asserts/4.jpg")
    # img5 = cv2.imread("asserts/5.jpg")
    # img6 = cv2.imread("asserts/6.jpg")
    # img7 = cv2.imread("asserts/7.jpg")

    member = [img1, img2, img3, img4, img5, img6, img7]

    # 检测第一张图中的人脸
    res, detectedFaces1 = face_engine.ASFDetectFaces(np.array(fram))
    print(detectedFaces1)
    if res == MOK:
        single_detected_face1 = ASF_SingleFaceInfo()
        single_detected_face1.faceRect = detectedFaces1.faceRect[0]
        single_detected_face1.faceOrient = detectedFaces1.faceOrient[0]
        res, face_feature1 = face_engine.ASFFaceFeatureExtract(np.array(fram), single_detected_face1)
        if (res != MOK):
            print("ASFFaceFeatureExtract 1 fail: {}".format(res))
    else:
        print("ASFDetectFaces 1 fail: {}".format(res))
    # arr = ['今天', '双11', '你剁手了吗'];
    # for value in arr:
    #     print(value)
    # # 检测第二张图中的人脸
    for value in member:

        # print("value"+value)
        res, detectedFaces2 = face_engine.ASFDetectFaces(value)
        if res == MOK:
            single_detected_face2 = ASF_SingleFaceInfo()
            single_detected_face2.faceRect = detectedFaces2.faceRect[0]
            single_detected_face2.faceOrient = detectedFaces2.faceOrient[0]
            res, face_feature2 = face_engine.ASFFaceFeatureExtract(value, single_detected_face2)
            if (res == MOK):
                pass
            else:
                print("ASFFaceFeatureExtract 2 fail: {}".format(res))
        else:
            print("ASFDetectFaces 2 fail: {}".format(res))

    # 比较两个人脸的相似度
        res, score = face_engine.ASFFaceFeatureCompare(face_feature1, face_feature2)
        print("相似度:", score)
        if cv2.waitKey(24) & 0xff == 27:
            break

HKIPcamera.release()

#
# # 设置活体置信度 SDK内部默认值为 IR：0.7 RGB：0.75（无特殊需要，可以不设置）
# threshold = ASF_LivenessThreshold()
# threshold.thresholdmodel_BGR = 0.75
# threshold.thresholdmodel_IR = 0.7
#
# face_engine.ASFSetLivenessParam(threshold)
#
# # RGB图像属性检测 注意:processMask中的内容必须在初始化引擎 时指定的功能内
# processMask = ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS
#
# res = face_engine.ASFProcess(img1, detectedFaces1, processMask)
#
# if res == MOK:
#     # 获取年龄
#     res, ageInfo = face_engine.ASFGetAge()
#     if (res != MOK):
#         print("ASFGetAge fail: {}".format(res))
#     else:
#         print("Age: {}".format(ageInfo.ageArray[0]))
#
#     # 获取性别
#     res, genderInfo = face_engine.ASFGetGender()
#     if (res != MOK):
#         print("ASFGetGender fail: {}".format(res))
#     else:
#         print("Gender: {}".format(genderInfo.genderArray[0]))
#
#     # 获取3D角度
#     res, angleInfo = face_engine.ASFGetFace3DAngle()
#     if (res != MOK):
#         print("ASFGetFace3DAngle fail: {}".format(res))
#     else:
#         print("3DAngle roll: {} yaw: {} pitch: {}".format(angleInfo.roll[0],
#                                                           angleInfo.yaw[0], angleInfo.pitch[0]))
#
#     # 获取RGB活体信息
#     res, rgbLivenessInfo = face_engine.ASFGetLivenessScore()
#     if (res != MOK):
#         print("ASFGetLivenessScore fail: {}".format(res))
#     else:
#         print("RGB Liveness: {}".format(rgbLivenessInfo.isLive[0]))
# else:
#     print("ASFProcess fail: {}".format(res))
#
# # **************进行IR活体检测********************
# # opencv读图时会将灰度图读成RGB图，需要转换成GRAY图进行IR活体检测
# img3_gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
#
# res, detectedFaces3 = face_engine.ASFDetectFaces(img3)
#
# if (res != MOK):
#     print("ASFGetLivenessScore fail: {}".format(res))
#
# # IR 活体检测
# res = face_engine.ASFProcess_IR(img3_gray, detectedFaces3)
#
# if res == MOK:
#     # 获取IR识别结果
#     res, irLivenessInfo = face_engine.ASFGetLivenessScore_IR()
#     print(irLivenessInfo)
#     if (res != MOK):
#         print("ASFGetLivenessScore_IR fail: {}".format(res))
#     else:
#         print("IR Liveness: {}".format(irLivenessInfo.isLive[0]))
# else:
#     print("ASFProcess_IR fail: {}".format(res))
#
#     # 反初始化
# face_engine.ASFUninitEngine()
