# -*- coding: utf-8 -*-

#############################################
##      D415 Depth画像の表示
#############################################
import pyrealsense2 as rs
import numpy as np
import cv2
import smbus
import time                 #sleepするためにtimeモジュールをインポートする
import datetime

bus = smbus.SMBus(1)    ##I2C通信するためのモジュールsmbusのインスタンスを作成
adress = 0x51           #arduinoのサンプルプログラムで設定したI2Cチャンネル

# ストリーム(Color/Depth)の設定
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is:" , depth_scale)

cnt = 0

try:
    while True:
        # フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not depth_frame or not color_frame:
            continue
        color_image = np.asanyarray(color_frame.get_data())
        # Depth画像
        depth_color_frame = rs.colorizer().colorize(depth_frame)
        depth_color_image = np.asanyarray(depth_color_frame.get_data())

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())

        depth1 = depth_image[240,320].astype(float) #CENTER
        distance1 = depth1 * depth_scale
        depth2 = depth_image[240,50].astype(float) #LEFT
        distance2 = depth2 * depth_scale
        depth3 = depth_image[240,550].astype(float) #RIGHT
        distance3 = depth3 * depth_scale

        anodepth2 = depth_image[240,30].astype(float) #LEFT
        anodistance2 = anodepth2 * depth_scale
        anodepth3 = depth_image[240,550].astype(float) #RIGHT
        anodistance3 = anodepth3 * depth_scale
        
        print("LEFT (m): ", distance2)
        print("CENTER (m): ", distance1)
        print("RIGHT (m): ", distance3)

        #障害物検知

        if distance3 < 0.7:
         print("RIGHT Obstacle")
         print("Sending:","l")
         bus.write_byte(adress, ord('l'))

        elif distance3 < 0.5 and distance2 < 0.7:
         print("Both ends Obstacle")
         print("Sending:","b")
         bus.write_byte(adress, ord('b'))

        elif distance2 < 0.5:
         print("LEFT Obstacle")
         print("Sending:","r")
         bus.write_byte(adress, ord('r'))

        elif distance1 < 0.7:
         print("CENTER Obstacle")
         print("Sending:","l")
         bus.write_byte(adress, ord('l'))

        else:
         print("Sending:","f")
         bus.write_byte(adress, ord('f'))

        #障害物画像収集
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%02S')

        if cnt > 7 and anodistance3 < 0.7:
         print("RIGHT Obstacle")
         cv2.imwrite(
        '/home/nvidia/obstacle/right/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])
         time.sleep(0.2)

        elif cnt > 7 and anodistance2 < 0.7:
         print("LEFT Obstacle")
         cv2.imwrite(
        '/home/nvidia/obstacle/left/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])
         time.sleep(0.2)

        elif cnt > 7 and distance1 < 0.7:
         print("CENTER Obstacle")
         cv2.imwrite(
        '/home/nvidia/obstacle/center/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])
         time.sleep(0.2)

        else:
         print("Straight")
         cv2.imwrite(
        '/home/nvidia/obstacle/straight/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])
         time.sleep(0.2)

        # 表示
        images = np.hstack((color_image, depth_color_image))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        if cv2.waitKey(1) & 0xff == 27:
           print("Sending:","s")
           bus.write_byte(adress, ord('s'))
           break

        cnt += 1

finally:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()

