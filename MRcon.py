from pygame.locals import *
import pygame
import sys
import smbus                #I2C通信するためのモジュールsmbusをインポートする
import time                 #sleepするためにtimeモジュールをインポートする

pygame.init()    # Pygameを初期化
screen = pygame.display.set_mode((400, 330))    # 画面を作成
pygame.display.set_caption("keyboard event")    # タイトルを作成

bus = smbus.SMBus(1)    ##I2C通信するためのモジュールsmbusのインスタンスを作成
adress = 0x51           #arduinoのサンプルプログラムで設定したI2Cチャンネル


while True:
    screen.fill((0, 0, 0)) 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:  # キーを押したとき
            # ESCキーならスクリプトを終了
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            else:
                print("押されたキー = " + pygame.key.name(event.key))
                if pygame.key.name(event.key) == "up":
                 print("Sending:","f")
                 bus.write_byte(adress, ord('f'))
                elif pygame.key.name(event.key) == "down":
                 print("Sending:","b")
                 bus.write_byte(adress, ord('b'))
                elif pygame.key.name(event.key) == "right":
                 print("Sending:","r")
                 bus.write_byte(adress, ord('r'))
                elif pygame.key.name(event.key) == "left":
                 print("Sending:","l")
                 bus.write_byte(adress, ord('l'))
                elif pygame.key.name(event.key) == "return":
                 print("Sending:","s")
                 bus.write_byte(adress, ord('s'))
                else:
                    
        pygame.display.update()
