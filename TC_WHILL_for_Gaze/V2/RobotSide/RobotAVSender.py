# -*- coding: utf-8 -*-
# client.py

import socket
import cv2
import numpy as np
import pyaudio  # type: ignore
import threading

SERVER_IP = '10.150.14.192'
PORT_VIDEO1 = 8000
PORT_VIDEO2 = 8001
PORT_VIDEO3 = 8002
PORT_AUDIO = 8003
PORT_VIDEO4 = 8004
PORT_AUDIO2 = 8005

# 汎用映像送信（UDP）
def video_sender(camera_index, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cap = cv2.VideoCapture(camera_index)
    print(f"Sending video from camera {camera_index} to port {port}...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        if len(buffer) < 65507:
            sock.sendto(buffer, (SERVER_IP, port))

    cap.release()
    sock.close()

# 音声送信（TCPクライアント）
def audio_sender():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Connecting to server audio receiver...")
        client_socket.connect((SERVER_IP, PORT_AUDIO))
        print("Audio connection to server established.")
    except Exception as e:
        print(f"Audio sender connect error: {e}")
        return

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            client_socket.sendall(data)
    except Exception as e:
        print(f"Audio send error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()

# 映像受信（UDP）
def video_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT_VIDEO4))
    print("Receiving video from server...")

    while True:
        try:
            data, _ = sock.recvfrom(65536)
            frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
            if frame is not None:
                cv2.imshow("VideoFromServer", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        except Exception as e:
            print(f"Video receive error: {e}")
            break

    sock.close()
    cv2.destroyAllWindows()

# 音声受信（TCPサーバー）
def audio_receiver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', PORT_AUDIO2))
    server_socket.listen(1)
    print("Waiting for server audio connection...")
    conn, _ = server_socket.accept()
    print("Audio connection from server established.")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            stream.write(data)
    except Exception as e:
        print(f"Audio receive error: {e}")
    finally:
        conn.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        server_socket.close()

# スレッド起動
threading.Thread(target=video_sender, args=(0, PORT_VIDEO1)).start()
threading.Thread(target=video_sender, args=(2, PORT_VIDEO2)).start()
threading.Thread(target=video_sender, args=(3, PORT_VIDEO3)).start()
threading.Thread(target=audio_sender).start()
threading.Thread(target=video_receiver).start()
threading.Thread(target=audio_receiver).start()
