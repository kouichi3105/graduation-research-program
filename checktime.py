import obstacles_keras2_third as obstacles
import sys, os
from PIL import Image
import numpy as np
import cv2
import time
import datetime

image_size = 50
categories = [
    "center", "right" , "left" , "straight"]

def cnn():
    # 入力画像をNumpyに変換 --- (※2)
    X = []
    files = []
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((image_size, image_size))
    in_data = np.asarray(img)
    X.append(in_data)
    files.append(fname)
    X = np.array(X)

    # CNNのモデルを構築 --- (※3)
    model = obstacles.build_model(X.shape[1:])
    model.load_weights("./Obstacle_corridor_third/obstacles_third_model.hdf5")

    # データを予測 --- (※4)
    pre = model.predict(X)
    for i, p in enumerate(pre):
        y = p.argmax()
        print("+ 入力:", files[i])
        print("| 種類:", categories[y])

capture = cv2.VideoCapture(1)

capture.set(3,640) # 幅
capture.set(4,480) # 高さ
capture.set(5,30)  # FPS

cnt = 0

while True:
  t1 = time.time()
  ret, image = capture.read()
  if cnt > 10:
   #画像保存
   nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M')
   cv2.imwrite('./Obstacle_corridor_third/detect/' + nowtime + ".jpg",
   image , [cv2.IMWRITE_JPEG_QUALITY, 50])
   fname = './Obstacle_corridor_third/detect/' + nowtime + ".jpg"
   cnn()
   cnt = 0
  
  cv2.imshow("camera",image)
  if cv2.waitKey(10) > 0:
    break
  t2 = time.time()
  elapsed_time = t2-t1
  print(f"time：{elapsed_time}")
  print(cnt)
  cnt += 1

capture.release()
cv2.destroyAllWindows()


