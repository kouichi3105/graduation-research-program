#　CNNで学習したモデルを用いて障害物回避するコード（画像から直接行動を選択）

import obstacles_keras2_third as obstacles
import sys, os
from PIL import Image
import numpy as np
import cv2
import time
import datetime
import smbus

bus = smbus.SMBus(1)    ##I2C通信するためのモジュールsmbusのインスタンスを作成
adress = 0x51           #arduinoのサンプルプログラムで設定したI2Cチャンネル

image_size = 50
categories = [
    "center", "right" , "left" , "straight"]

capture = cv2.VideoCapture(1)

capture.set(3,640) # 幅
capture.set(4,480) # 高さ
capture.set(5,30)  # FPS

cnt = 0

while True:
  ret, image = capture.read()
  if cnt > 10:
   #画像保存
   # 入力画像をNumpyに変換 --- (※2)
    X = []
    files = []
    img = cv2.resize(image,(image_size, image_size))
    in_data = np.asarray(img)
    X.append(in_data)
    files.append(img)
    X = np.array(X)

    # CNNのモデルを構築 --- (※3)
    model = obstacles.build_model(X.shape[1:])
    model.load_weights("./Obstacle_corridor_third/obstacles_third_model.hdf5")

    # データを予測 --- (※4)
    pre = model.predict(X)
    for i, p in enumerate(pre):
        y = p.argmax()
        #print("+ 入力:", files[i])
        print("| 種類:", categories[y])

        #障害物検知
        if categories[y] == 'left':
         print("LEFT Obstacle")
         print("Sending:","r")
         bus.write_byte(adress, ord('r'))
         time.sleep(0.5)
         bus.write_byte(adress, ord('s'))
         print("Sending:","s")

        elif categories[y] == 'center':
         print("CENTER Obstacle")
         print("Sending:","l")
         bus.write_byte(adress, ord('l'))
         time.sleep(0.5)
         bus.write_byte(adress, ord('s'))
         print("Sending:","s")

        elif categories[y] == 'right':
         print("RIGHT Obstacle")
         print("Sending:","l")
         bus.write_byte(adress, ord('l'))
         time.sleep(0.5)
         bus.write_byte(adress, ord('s'))
         print("Sending:","s")

        else:
         print("Sending:","f")
         bus.write_byte(adress, ord('f'))
         #time.sleep(1)
         #bus.write_byte(adress, ord('s'))
         #print("Sending:","s")

        cnt = 0
  
  #cv2.imshow("camera",image)
  if cv2.waitKey(10) > 0:
    break

  cnt += 1

capture.release()
cv2.destroyAllWindows()


