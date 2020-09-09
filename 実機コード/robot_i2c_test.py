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
            key = input('命令を入力>>')

            if key == 'f':
                #Arduinoへ文字『f』を送る、ordはアスキーコードを取得
                print("Sending:","f")
                bus.write_byte(adress, ord('f'))
                time.sleep(1)

            elif key == 'r':
                #Arduinoへ文字『r』を送る、ordはアスキーコードを取得
                print("Sending:","r")
                bus.write_byte(adress, ord('r'))
                time.sleep(1)

            elif key == 'b':
                #Arduinoへ文字『b』を送る、ordはアスキーコードを取得
                print("Sending:","b")
                bus.write_byte(adress, ord('b'))
                time.sleep(1)

            elif key == 'l':
                #Arduinoへ文字『l』を送る、ordはアスキーコードを取得
                print("Sending:","l")
                bus.write_byte(adress, ord('l'))
                time.sleep(1)

            elif key == 's':
                #Arduinoへ文字『s』を送る、ordはアスキーコードを取得
                print("Sending:","s")
                bus.write_byte(adress, ord('s'))
                time.sleep(1)


    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
    except Exception as e:
        print(str(e))
    finally:
        print("\nexit program")
