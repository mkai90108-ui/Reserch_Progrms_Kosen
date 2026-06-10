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
#HOST = '192.168.56.1'
HOST = '0.0.0.0'
PORT = 8006

#ニンテンドーJoy-Conを使う場合に必要
VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

#画面サイズ
scr_w,scr_h= pag.size()

memresx=0
memresy=0
memresX=0
memresY=0
t=0

l=50

kirihan=0

old_rx = []
old_ry = []
old_lx = []
old_ly = []

gaze_data_list = []
right_eye_x = []
right_eye_y = []
left_eye_x = []
left_eye_y = []
px=scr_w//2+150
py=scr_h//2

oldc=0

rex=0
rey=0
lex=0
ley=0

px10=scr_w//2+150
py10=scr_h//2

px10kai=scr_w//2+150
py10kai=scr_h//2

px10kai2=scr_w//2+150
py10kai2=scr_h//2

px10kai3=scr_w//2+150
py10kai3=scr_h//2

px10kai4=scr_w//2+150
py10kai4=scr_h//2
oldc3=0

px18=scr_w//2+150
py18=scr_h//2

px60=scr_w//2+150
py60=scr_h//2

TZ=' '
T_x=scr_w//2+150
T_y=scr_h//2
o=0
T=0
root = tk.Tk()

oldz=0
oldc4=0

oldc2=0
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

comcounter=[0,0,0,0,0]

kirikae=0

#視線データのメモリ初期化
for i in range(60):
    old_rx.append(0.5)
    old_ry.append(0.7)
    old_lx.append(0.5)
    old_ly.append(0.7)

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



def nanhan(x):
    if(x==float('nan')):
        x=0.5
    return x
        
        
def pointthink(px,py,kaityo):
    
    if((py<=2*int(scr_h/5)+20)and(px>=int(scr_w/6))and(px<=int(scr_w/6*5))):
        if (kaityo==1):
            #sigmo
            x=int(20/(1+math.exp(-(((scr_h/2-py)-(scr_h/2-(2*int(scr_h/5)+20)))-250)/70)))
        elif (kaityo==2):
            #fefina
            x=int(4.33*math.log(((scr_h/2-py)-(scr_h/2-(2*int(scr_h/5)+20)))/4+1))
        elif (kaityo==3):
            #heihou
            #x=int(math.sqrt(((scr_h/2-py)-(scr_h/2-(2*int(scr_h/5)+20)))/2))
            x=int(math.sqrt(((scr_h/2-py)-(scr_h/2-(2*int(scr_h/5)+20)))/1.1))
        elif (kaityo==4):
            #指数h
            x=int(math.exp((((scr_h/2-py)-(scr_h/2-(2*int(scr_h/5)+20)))/4+1)/(4.33*5)))
        elif (kaityo==5):
            #指数A
            x=int(math.exp((((scr_h/2-py)-(scr_h/2-(2*int(scr_h/5)+20)))/4+1)/(4.33*9)))
        else:
            #hirei
            x=int((20/(2*(scr_h/5+20)))*((scr_h/2-py)-(scr_h/2-(2*int(scr_h/5)+20))))
            
            
        y=-int((30/(scr_w/2))*(scr_w/2-px))
        if x>20:
            x = 20
        if y>30:
            y = 30
        if y<-30:
            y = -30
        z='前'
    elif((py<=2*int(scr_h/5)+20)and(px<=int(scr_w/6))):
        x=0
        y=-int((30/(scr_w/2))*(scr_w/2-px))
        if y>30:
            y = 30
        if y<-30:
            y = -30
        z='左旋回'
    elif((py<=2*int(scr_h/5)+20)and(px>=int(scr_w/6*5))):
        x=0
        y=-int((30/(scr_w/2))*(scr_w/2-px))
        if y>30:
            y = 30
        if y<-30:
            y = -30
        z='右旋回'
    elif((px<=scr_w-int(scr_w/3-20)) and (py>=scr_h-int(scr_h/5)-20)and(px>=int(scr_w/3-20))):
        x=-50
        y=0
        z='後退'
    else:
        x=0
        y=0
        z='停止'
        
    
    return z,x,y

def plthink(px,py):
    
    if((py<=2*int(scr_h/5)+20)and(px>=int(scr_w/6))and(px<=int(scr_w/6*5))):

        z=1
    elif((py<=2*int(scr_h/5)+20)and(px<=int(scr_w/6))):

        z=2
    elif((py<=2*int(scr_h/5)+20)and(px>=int(scr_w/6*5))):

        z=3
    elif((px<=scr_w-int(scr_w/3-20)) and (py>=scr_h-int(scr_h/5)-20)and(px>=int(scr_w/3-20))):

        z=4
    else:

        z=0
        
    
    return z
    
def lenthink(ax,ay,bx,by,oc,nc):
    cz=[]
    for i in range(len(ax)):
        cx=(ax[i]+bx[i])/2*scr_w
        cy=(ay[i]+by[i])/2*scr_h
        cz.append(plthink(cx,cy))
    if(cz.count(nc)>cz.count(oc)):
        return True
    else:
        return False
    
        
def lenthink2(ax,ay,bx,by,oc,nc,a):
    cz=[]
    for i in range(len(ax)):
        cx=(ax[i]+bx[i])/2*scr_w
        cy=(ay[i]+by[i])/2*scr_h
        cz.append(plthink(cx,cy))
    if((cz.count(nc)>a[nc]+12)and(cz.count(oc)<a[oc]-12)):
        a=[]
        a.append(cz.count(0))
        a.append(cz.count(1))
        a.append(cz.count(2))
        a.append(cz.count(3))
        a.append(cz.count(4))
        return True,a
    else:
        a=[]
        a.append(cz.count(0))
        a.append(cz.count(1))
        a.append(cz.count(2))
        a.append(cz.count(3))
        a.append(cz.count(4))
        return False,a
    




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
            
            status_window = tk.Toplevel(root)
            status_window.title("現在のモード")
            status_window.geometry("500x500")

            canvas = tk.Canvas(root,width=scr_w,height=scr_h,background="snow")

            canvas.pack(fill = tk.BOTH, expand = True)

            #label=tk.Label(master=root,text="●",font=("Helvetica",20),foreground="red",background="snow")
            label1=tk.Label(master=status_window, text="3比例", font=("Helvetica", 30), foreground="green", wraplength=480)
            label2=tk.Label(master=status_window, text="1log", font=("Helvetica", 30), foreground="green", wraplength=480)
            label3=tk.Label(master=status_window, text="5シグモイド", font=("Helvetica", 30), foreground="green", wraplength=480)
            label4=tk.Label(master=status_window, text="2ルート", font=("Helvetica", 30), foreground="green", wraplength=480)
            label5=tk.Label(master=status_window, text="4指数h", font=("Helvetica", 30), foreground="green", wraplength=480)
            label6=tk.Label(master=status_window, text="6指数A", font=("Helvetica", 30), foreground="green", wraplength=480)
            
            #label.place(x=150,y=150)
            canvas.create_line(int(scr_w/3-20),scr_h-int(scr_h/5)-20, int(scr_w/3-20), scr_h, fill = "Blue", width = 5)
            canvas.create_line(scr_w-int(scr_w/3-20),scr_h-int(scr_h/5)-20, scr_w-int(scr_w/3-20), scr_h, fill = "Blue", width = 5)
            canvas.create_line(int(scr_w/6),1, int(scr_w/6), 2*int(scr_h/5)+20, fill = "Blue", width = 5)
            canvas.create_line(int(scr_w/6*5),1, int(scr_w/6*5), 2*int(scr_h/5)+20, fill = "Blue", width = 5)
            canvas.create_line(scr_w-int(scr_w/3-20),scr_h-int(scr_h/5)-20, int(scr_w/3-20), scr_h-int(scr_h/5)-20, fill = "Blue", width = 5)
            canvas.create_line(1,2*int(scr_h/5)+20, scr_w, 2*int(scr_h/5)+20, fill = "Blue", width = 5)
            
            with open('C:/Users/kaibh\Downloads/xF2.csv', 'w') as f:
                with open('C:/Users/kaibh\Downloads/xF60hz.csv', 'w') as f2:
                    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback,as_dictionary=True)
                    while True:
                        canvas.create_oval(T_x+50,T_y+50,T_x-50,T_y-50,outline = "snow", width = 5)
                        if keyboard.is_pressed("space"):
                            break
                        
                        if (not(keyboard.is_pressed("s"))):
                            kirihan=0
                        if (keyboard.is_pressed("s") and kirihan == 0):
                            kirikae=kirikae+1
                            if kirikae>5:
                                kirikae=0
                            kirihan = 1
                        start_t=time.time()
                        writer = csv.writer(f)
                        writer2 = csv.writer(f2)
                        start_gt=time.time()
                        

                    # 視線データを0.1秒間だけ取得
                        time.sleep(0.3)

                    # 接続を閉じる
                        end_gt =time.time()
                        
                        for data in gaze_data_list:
                            right_eye_x.append(data['right_gaze_point_on_display_area'][0])
                            right_eye_y.append(data['right_gaze_point_on_display_area'][1])
                            left_eye_x.append(data['right_gaze_point_on_display_area'][0])
                            left_eye_y.append(data['right_gaze_point_on_display_area'][1])
                        gaze_data_list = []
                        
                        if(o==1):
                        
                            del old_rx[0:len(right_eye_x)]
                            del old_ry[0:len(right_eye_y)]
                            del old_lx[0:len(left_eye_x)]
                            del old_ly[0:len(left_eye_y)]
                            
                            old_rx=old_rx+right_eye_x
                            old_ry=old_ry+right_eye_y
                            old_lx=old_lx+left_eye_x
                            old_ly=old_ly+left_eye_y
                            
                            rx=np.nanmean(old_rx)
                            ry=np.nanmean(old_ry)
                            lx=np.nanmean(old_lx)
                            ly=np.nanmean(old_ly)
                            
                            x=(rx+lx)/2*scr_w
                            y=(ry+ly)/2*scr_h
                            
                            
                            if(math.isnan(x) == False):
                                print(x,y,scr_h,scr_w)
                                px60=int(x)
                                py60=int(y)
                            
                            [Z60, X60, Y60]=pointthink(px60,py60,kirikae)
                                
                            rx=np.nanmean(right_eye_x[-10:-1])
                            ry=np.nanmean(right_eye_y[-10:-1])
                            lx=np.nanmean(left_eye_x[-10:-1])
                            ly=np.nanmean(left_eye_y[-10:-1])
                            
                            x=(rx+lx)/2*scr_w
                            y=(ry+ly)/2*scr_h
                            
                            
                            if(math.isnan(x) == False):
                                print(x,y,scr_h,scr_w)
                                px10=int(x)
                                py10=int(y)
                            [Z10,X10,Y10]=pointthink(px10,py10,kirikae)
                            
                            rx=np.nanmean(right_eye_x)
                            ry=np.nanmean(right_eye_y)
                            lx=np.nanmean(left_eye_x)
                            ly=np.nanmean(left_eye_y)
                            
                            x=(rx+lx)/2*scr_w
                            y=(ry+ly)/2*scr_h
                        
                        
                        
                            if(math.isnan(x) == False):
                                print(x,y,scr_h,scr_w)
                                px18=int(x)
                                py18=int(y)
                            [Z18,X18,Y18]=pointthink(px18,py18,kirikae)

                            newc=plthink(px10,py10)
                            print(oldc)
                            print(newc)
                            if(lenthink(old_rx,old_ry,old_lx,old_ly,oldc,newc)or(oldc==newc)):
                                px10kai=px10
                                py10kai=py10
                                oldc=newc
                            [Z10kai,X10kai,Y10kai]=pointthink(px10kai,py10kai,kirikae)
                            
                            if(lenthink(old_rx[-30:-1],old_ry[-30:-1],old_lx[-30:-1],old_ly[-30:-1],oldc2,newc)or(oldc2==newc)):
                                px10kai2=px10
                                py10kai2=py10
                                oldc2=newc
                            [Z10kai2,X10kai2,Y10kai2]=pointthink(px10kai2,py10kai2,kirikae)
                            
                            if(lenthink(old_rx[-18:-1],old_ry[-18:-1],old_lx[-18:-1],old_ly[-18:-1],oldc3,newc)or(oldc3==newc)):
                                px10kai3=px10
                                py10kai3=py10
                                oldc3=newc
                            [Z10kai3,X10kai3,Y10kai3]=pointthink(px10kai3,py10kai3,kirikae)
                            
                            #[ans,comcounter]=lenthink2(old_rx,old_ry,old_lx,old_ly,oldc4,newc,comcounter)
                            #if(ans or(oldc4==newc)):
                            if(lenthink(old_rx,old_ry,old_lx,old_ly,oldc4,newc) or(oldc4==newc)):
                                px10kai4=px10
                                py10kai4=py10
                                oldc4=newc
                            [Z10kai4,X10kai4,Y10kai4]=pointthink(px10kai4,py10kai4,kirikae)                            
                            
                            if(o==1):
                                T_rx=np.nanmean(right_eye_x[-1])
                                T_ry=np.nanmean(right_eye_y[-1])
                                T_lx=np.nanmean(left_eye_x[-1])
                                T_ly=np.nanmean(left_eye_y[-1])
                                
                                T_x=(T_rx+T_lx)/2*scr_w
                                T_y=(T_ry+T_ly)/2*scr_h
                                
                                
                                if(math.isnan(T_x) == False):
                                    T_x=int(T_x)
                                    T_y=int(T_y)
                                    
                                
                            #label.place(x=T_x,y=T_y)
                            canvas.create_line(int(scr_w/3-20),scr_h-int(scr_h/5)-20, int(scr_w/3-20), scr_h, fill = "Blue", width = 5)
                            canvas.create_line(scr_w-int(scr_w/3-20),scr_h-int(scr_h/5)-20, scr_w-int(scr_w/3-20), scr_h, fill = "Blue", width = 5)
                            canvas.create_line(int(scr_w/6),1, int(scr_w/6), 2*int(scr_h/5)+20, fill = "Blue", width = 5)
                            canvas.create_line(int(scr_w/6*5),1, int(scr_w/6*5), 2*int(scr_h/5)+20, fill = "Blue", width = 5)
                            canvas.create_line(scr_w-int(scr_w/3-20),scr_h-int(scr_h/5)-20, int(scr_w/3-20), scr_h-int(scr_h/5)-20, fill = "Blue", width = 5)
                            canvas.create_line(1,2*int(scr_h/5)+20, scr_w, 2*int(scr_h/5)+20, fill = "Blue", width = 5)
                            canvas.create_oval(T_x+50,T_y+50,T_x-50,T_y-50,outline = "Red", width = 5)
                            
                            if(kirikae==1):
                                label1.place(x=-500,y=-1000)
                                label2.place(x=-500,y=-1000)
                                label3.place(x=250,y=250)
                                label4.place(x=-500,y=-1000)
                                label5.place(x=-500,y=-1000)
                                label6.place(x=-500,y=-1000)
                                Sk="sigmo"
                            elif(kirikae==2):
                                label1.place(x=-500,y=-1000)
                                label2.place(x=250,y=250)
                                label3.place(x=-500,y=-1000)
                                label4.place(x=-500,y=-1000)
                                label5.place(x=-500,y=-1000)
                                label6.place(x=-500,y=-1000)
                                Sk="fefinar"
                            elif(kirikae==3):
                                label1.place(x=-500,y=-1000)
                                label2.place(x=-500,y=-1000)
                                label3.place(x=-500,y=-1000)
                                label4.place(x=250,y=250)
                                label5.place(x=-500,y=-1000)
                                label6.place(x=-500,y=-1000)
                                Sk="heihou"
                            elif(kirikae==4):
                                label1.place(x=-500,y=-1000)
                                label2.place(x=-500,y=-1000)
                                label3.place(x=-500,y=-1000)
                                label4.place(x=-500,y=-1000)
                                label5.place(x=250,y=250)
                                label6.place(x=-500,y=-1000)
                                Sk="sisuh"
                            elif(kirikae==5):
                                label1.place(x=-500,y=-1000)
                                label2.place(x=-500,y=-1000)
                                label3.place(x=-500,y=-1000)
                                label4.place(x=-500,y=-1000)
                                label5.place(x=-500,y=-1000)
                                label6.place(x=250,y=250)
                                Sk="sisuA"
                            else:
                                label1.place(x=250,y=250)
                                label2.place(x=-500,y=-1000)
                                label3.place(x=-500,y=-1000)
                                label4.place(x=-500,y=-1000)
                                label5.place(x=-500,y=-1000)
                                label6.place(x=-500,y=-1000)
                                Sk="hirei"
                            
                            #[X,Y,Z] = pointjoy(Y10kai4,X10kai4)

                            x=int_to_4_digit_string(minas_int(int(X10kai4)))
                            y=int_to_4_digit_string(minas_int(int(Y10kai4)))
                                

                            response1=str(y+x+"00000\n")
                            dt_now = datetime.datetime.now()
                            
                            if(t>=3):
                                t=0
                                
                            if (((memresx!=px10kai4 or memresy!=py10kai4) and t==0)or (memresX!=X10kai4 or memresY!=Y10kai4)):    
                                client_socket.send(response1.encode('utf-8'))
                                print(response1)
                                print(X10kai4)
                                print(Y10kai4)
                                memresX=X10kai4
                                memresY=Y10kai4
                                t=0
                            end_t =time.time()
                            
                            
                        
                                
                            memresx=px10kai4
                            memresy=py10kai4
                            print('======')
                            print(memresX)
                            print(X10kai4)
                            print(memresx)
                            print(memresy)
                            print('------')
                            
                            root.update()
                            
                            
                            end_t =time.time()
                            test_time=end_t-start_t
                            test_gtime=end_gt-start_gt
                            list_len=len(right_eye_x)
                            T=T+test_time
                            writer.writerow([T,T_x, T_y,Z10,X10,Y10,px10,py10,Z18,X18,Y18,px18,py18,Z60,X60,Y60,px60,py60,Z10kai,X10kai,Y10kai,px10kai,py10kai,Z10kai2,X10kai2,Y10kai2,px10kai2,py10kai2,Z10kai3,X10kai3,Y10kai3,px10kai3,py10kai3,Z10kai4,X10kai4,Y10kai4,px10kai4,py10kai4,Sk])
                            for i in range(len(right_eye_x)):
                                
                                if(math.isnan(right_eye_x[i]) == False):
                                    rex=np.nanmean(right_eye_x[i])
                                    rey=np.nanmean(right_eye_y[i])
                                    lex=np.nanmean(left_eye_x[i])
                                    ley=np.nanmean(left_eye_y[i])
                                writer2.writerow([int((rex+lex)/2*scr_w),int((rey+ley)/2*scr_h),T])
                            right_eye_x = []
                            right_eye_y = []
                            left_eye_x = []
                            left_eye_y = []
                        o=1
                        t=t+1
                    
            root.mainloop()