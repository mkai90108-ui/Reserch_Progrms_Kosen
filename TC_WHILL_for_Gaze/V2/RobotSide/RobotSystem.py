# -*- coding: utf-8 -*-


import socket
from whill import ComWHILL
import select
import keyboard
import time
# ソケット通信の設定
HOST = '10.150.14.192'
PORT = 8006
BUFSIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send("Hi pi".encode())

# WHILL の初期化
mainobj = ComWHILL('COM4')

def controllW(F, S):
    mainobj.send_joystick(front=F, side=S)

# 初期値
x = 1000
y = 1000
move_x=0
move_y=0
i=0
p=0


time.sleep(0.1)
mainobj.send_power_on()

while True:
    if keyboard.is_pressed("space"):
        break
    
    if(i>=10):
        move_y=0
        move_x=0
    controllW(int(move_y), int(move_x))
    print(move_x)
    print(move_y)
    # 受信チェック（0.1秒以内にデータがなければスキップ）
    ready, _, _ = select.select([client], [], [], 0.1)
    if not ready:
        i=i+1
        continue  # データが来ていなければループの先頭へ戻る
    i=0
    data = client.recv(BUFSIZE).decode()
    print(data)

    try:
        x, y = int(data[:4]), int(data[4:8])
    except ValueError:
        print("Invalid data:", data)
        continue  # 不正なデータを無視
    print(x, y)

    if(x==1000 and y==1000):
        move_x=0
        move_y=0
    else:
        if(x>=1000):
            move_x=0-x+1000
        else:
            move_x=x
        if(y>=1000):
            move_y=0-y+1000
        else:
            move_y=y

    if keyboard.is_pressed('w'):
        move_x=10
    elif keyboard.is_pressed('s'):
        move_x=-10
    if keyboard.is_pressed('d'):
        move_y=50
    elif keyboard.is_pressed('a'):
        move_y=-50
    print(move_x, move_y)
    controllW(move_x, move_y)

mainobj.send_power_off()
