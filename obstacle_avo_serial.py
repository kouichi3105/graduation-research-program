# -*- coding: utf-8 -*-

#############################################
##      D415 Depth画像の表示
#############################################
import pyrealsense2 as rs
import numpy as np
import cv2
import serial
import time                 #sleepするためにtimeモジュールをインポートする
import datetime

with serial.Serial('COM6',9600,timeout=1) as ser:

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

def go():
  print("Sending:","f")
  data=bytes('f','utf-8')
  ser.write(data)

def right():
  print("Sending:","r")
  data=bytes('r','utf-8')
  ser.write(data)

def left():
  print("Sending:","l")
  data=bytes('l','utf-8')
  ser.write(data)

def center():
  print("Sending:","l")
  data=bytes('l','utf-8')
  ser.write(data)

def back():
  print("Both ends Obstacle")
  data=bytes('b','utf-8')
  ser.write(data)

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

        cdepth = depth_image[240,320].astype(float) #CENTER
        cdistance = cdepth * depth_scale
        ldepth1 = depth_image[240,64].astype(float) #LEFT1
        ldistance1 = ldepth1 * depth_scale
        ldepth2 = depth_image[240,192].astype(float) #LEFT2
        ldistance2 = ldepth2 * depth_scale
        rdepth1 = depth_image[240,576].astype(float) #RIGHT1
        rdistance1 = rdepth1 * depth_scale
        rdepth2 = depth_image[240,448].astype(float) #RIGHT2
        rdistance2 = rdepth2 * depth_scale

        print("LEFT1 (m): ", ldistance1)
        print("LEFT2 (m): ", ldistance2)
        print("CENTER (m): ", cdistance)
        print("RIGHT1 (m): ", rdistance1)
        print("RIGHT2 (m): ", rdistance2)

        #障害物検知
        if rdistance2 < 0.6:
         right()

        elif rdistance1 < 0.5:
         right()

        elif ldistance2 < 0.6:
         left()

        elif cdistance < 0.5:
         center()

        elif ldistance1 < 0.5:
         left()

        else:
         go()

        #障害物画像収集
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%02S')

        if cnt > 7 and rdistance1 < 0.6:
         print("RIGHT Obstacle")
         '''cv2.imwrite(
        '/home/nvidia/obstacle/right/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])
         
         cv2.imwrite(
        '/home/nvidia/obstacle/right2/' + now_time + ".jpg",
        depth_color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])'''
         time.sleep(0.4)

        elif cnt > 7 and rdistance2 < 0.65:
         print("RIGHT Obstacle")
         '''cv2.imwrite(
        '/home/nvidia/obstacle/right/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])
         
         cv2.imwrite(
        '/home/nvidia/obstacle/right2/' + now_time + ".jpg",
        depth_color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])'''
         time.sleep(0.4)

        elif cnt > 7 and ldistance1 < 0.6:
         print("LEFT Obstacle")
         '''cv2.imwrite(
        '/home/nvidia/obstacle/left/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])

         cv2.imwrite(
        '/home/nvidia/obstacle/left2/' + now_time + ".jpg",
        depth_color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])'''
         time.sleep(0.4)

        elif cnt > 7 and ldistance2 < 0.65:
         print("LEFT Obstacle")
         '''cv2.imwrite(
        '/home/nvidia/obstacle/left/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])

         cv2.imwrite(
        '/home/nvidia/obstacle/left2/' + now_time + ".jpg",
        depth_color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])'''
         time.sleep(0.4)

        elif cnt > 7 and cdistance < 0.7:
         print("CENTER Obstacle")
         '''cv2.imwrite(
        '/home/nvidia/obstacle/center/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])

         cv2.imwrite(
        '/home/nvidia/obstacle/center2/' + now_time + ".jpg",
        depth_color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])'''
         time.sleep(0.3)

        else:
         print("Straight")
         '''cv2.imwrite(
        '/home/nvidia/obstacle/straight/' + now_time + ".jpg",
        color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])

         cv2.imwrite(
        '/home/nvidia/obstacle/straight2/' + now_time + ".jpg",
        depth_color_image , [cv2.IMWRITE_JPEG_QUALITY, 50])'''
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

