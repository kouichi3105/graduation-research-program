#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smbus                #I2C通信するためのモジュールsmbusをインポートする
import time                 #sleepするためにtimeモジュールをインポートする

"""メイン関数"""
if __name__ == '__main__':
    bus = smbus.SMBus(1)    ##I2C通信するためのモジュールsmbusのインスタンスを作成
    adress = 0x51           #arduinoのサンプルプログラムで設定したI2Cチャンネル

    try:
        while True:
            #Arduinoへ文字『f』を送る、ordはアスキーコードを取得
            bus.write_byte(adress, ord('f'))

            #0.5sスリープする
            time.sleep(10)

            #Arduinoへ文字『s』を送る、ordはアスキーコードを取得
            bus.write_byte(adress, ord('s'))

    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
    except Exception as e:
        print(str(e))
    finally:
        print("\nexit program")
