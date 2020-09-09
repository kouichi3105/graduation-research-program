#3 CNN画像分類予測コード　
# コマンドラインにobstacles_checker_third.py 推定する画像名.jpg と入力する

import obstacles_keras2_third as obstacles
import sys, os
from PIL import Image
import numpy as np

# コマンドラインからファイル名を得る --- (※1)
if len(sys.argv) <= 1:
    print("obstacles-checker-third.py (ファイル名)")
    quit()

image_size = 50
categories = [
    "center", "right" , "left" , "straight"]


# 入力画像をNumpyに変換 --- (※2)
X = []
files = []
for fname in sys.argv[1:]:
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
    
    

