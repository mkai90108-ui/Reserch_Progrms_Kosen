import socket
import tobii_research as tr 
import time
import hid
import math
import tkinter
import keyboard
import pyautogui as pag
import tkinter as tk
import csv
import numpy as np
import datetime
#import webbrowser

# サーバのIPアドレスとポート番号を設定
HOST = '10.150.19.249'
#HOST = '192.168.11.3'
PORT = 8000

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

scr_w,scr_h= pag.size()

memresx=0
memresy=0
memres="1000100000000"
t=0

l=50

gaze_data_list = []
right_eye_x = []
right_eye_y = []
left_eye_x = []
left_eye_y = []
px=scr_w//2+150
py=scr_h//2

root = tk.Tk()

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

def gaze_data_callback(gaze_data):
    gaze_data_list.append(gaze_data)

def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)

def int_to_4_digit_string(number):
    # 整数を4桁の文字列に変換し、ゼロで埋める
    result = f"{number:04}"
    return result

def minas_int(number):
    if(0>=number):
        number=1000-number
    return number

def pointjoy(px,py):
    
    if(py<=2*int(scr_h/5)+100):
        x=int((200/(scr_h/5))*(scr_h/2-py))
        y=-int((100/(scr_w/2))*(scr_w/2-px))
        if x>100:
            x = 100
        if y>100:
            y = 100
        if y<-100:
            y = -100
        z='前'
    elif((py>=2*int(scr_h/5)+100) and (px<=int(scr_w/3-100))):
        x=0
        y=-100
        z='左旋回'
    elif((py>=2*int(scr_h/5)+100) and (px>=scr_w-int(scr_w/3-100))):
        x=0
        y=100
        z='右旋回'
    elif((px<=scr_w-int(scr_w/3-100)) and (py>=scr_h-int(scr_h/5)+100)and(px>=int(scr_w/3-100))):
        x=-100
        y=0
        z='後退'
    else:
        x=0
        y=0
        z='停止'
        
    
    return x,y,z

def nanhan(x):
    if(x==float('nan')):
        x=0.5
    return x
        
    





# ソケットを作成し、指定したIPアドレスとポート番号でバインド

while True:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    # クライアントからの接続を待ち受け
    server_socket.listen()


    print(f"サーバが {HOST}:{PORT} で待機中...")

    # クライアントからの接続を受け入れる
    client_socket, client_address = server_socket.accept()
    print(f"クライアント {client_address} が接続しました。")
        # クライアントからのデータを受信
    data = client_socket.recv(1024)
    if not data:
        client_socket.close()
        server_socket.close()

    # 受信したデータを表示
    print(f"受信したメッセージ: {data.decode()}")

    # クライアントにデータを返信
    response = "サーバからの応答: メッセージを受信しました。" 
    client_socket.send(response.encode())

    #url = 'http://'+'192.168.11.10'+":"+"8080"
        
    #webbrowser.open(url)

    time.sleep(0.01)
    
    while True:
        if keyboard.read_key() == "s":
            
            root.wm_attributes("-transparentcolor", "snow")
            root.attributes('-fullscreen', True)
            #root.attributes("-alpha",0.5)
            root.wm_attributes("-transparentcolor", "snow")
            root.attributes('-fullscreen', True)
            #root.attributes("-alpha",0.5)
            tk.Frame(root, background="snow").pack(expand=True, fill=tk.BOTH)

            canvas = tk.Canvas(root,width=scr_w,height=scr_h,background="snow")

            canvas.pack(fill = tk.BOTH, expand = True)

            label=tk.Label(master=root,text="●",font=("Helvetica",20),foreground="red",background="snow")
            #label.place(x=150,y=150)
            
            canvas.create_line(int(scr_w/3-100),2*int(scr_h/5)+100, int(scr_w/3-100), scr_h, fill = "Blue", width = 5)
            canvas.create_line(scr_w-int(scr_w/3-100),2*int(scr_h/5)+100, scr_w-int(scr_w/3-100), scr_h, fill = "Blue", width = 5)
            canvas.create_line(scr_w-int(scr_w/3-100),scr_h-int(scr_h/5)+100, int(scr_w/3-100), scr_h-int(scr_h/5)+100, fill = "Blue", width = 5)
            canvas.create_line(1,2*int(scr_h/5)+100, scr_w, 2*int(scr_h/5)+100, fill = "Blue", width = 5)
            
            with open('C:/Users/kaibh\Downloads/Honban1.csv', 'w') as f:
                my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback,as_dictionary=True)
                while True:
                    
                    start_t=time.time()
                    writer = csv.writer(f)
                    start_gt=time.time()
                    

                # 視線データを0.9秒間だけ取得
                    time.sleep(0.3)

                # 接続を閉じる
                    end_gt =time.time()
                    
                    for data in gaze_data_list:
                        right_eye_x.append(data['right_gaze_point_on_display_area'][0])
                        right_eye_y.append(data['right_gaze_point_on_display_area'][1])
                        left_eye_x.append(data['right_gaze_point_on_display_area'][0])
                        left_eye_y.append(data['right_gaze_point_on_display_area'][1])
                    gaze_data_list = []
                    print(len(right_eye_x))
                    rx=np.nanmean(right_eye_x[-10:-1])
                    ry=np.nanmean(right_eye_y[-10:-1])
                    lx=np.nanmean(left_eye_x[-10:-1])
                    ly=np.nanmean(left_eye_y[-10:-1])
                    
                    x=(rx+lx)/2*scr_w
                    y=(ry+ly)/2*scr_h
                    
                    print('A')
                    
                    if(math.isnan(x) == False):
                        print(x,y,scr_h,scr_w)
                        px=int(x)
                        py=int(y)
                        
                    label.place(x=py,y=px)
                    
                    [X,Y,Z] = pointjoy(px,py)

                    x=int_to_4_digit_string(minas_int(int(X)))
                    y=int_to_4_digit_string(minas_int(int(Y)))
                        

                    response1=str(y+x+"00000\n")
                    dt_now = datetime.datetime.now()
                    T=dt_now.strftime('%H:%M:%S')
                        
                    if ((memresx!=px and memresy!=py and t==0)or memres!=response1):    
                        client_socket.send(response1.encode('utf-8'))
                        print(response1)
                        memres=response1
                        t=0
                    end_t =time.time()
                    
                    test_time=end_t-start_t
                    test_gtime=end_gt-start_gt
                    list_len=len(right_eye_x)
                    writer.writerow([T,Z,px,py,list_len,test_time,test_gtime])
                    
                    t=t+1
                    
                    if(t>=3):
                        t=0
                        
                    memresx=px
                    memresy=py
                    
                    label.place(x=px,y=py)
                    root.update()
                    
                    right_eye_x = []
                    right_eye_y = []
                    left_eye_x = []
                    left_eye_y = []
                    
                    
            root.mainloop()