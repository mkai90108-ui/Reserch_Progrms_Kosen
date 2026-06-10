# server.py
import socket
import cv2
import numpy as np
import pyaudio
import threading

HOST = '0.0.0.0'
CLIENT_IP = '10.150.15.24'
PORT_VIDEO1 = 8000
PORT_VIDEO2 = 8001
PORT_VIDEO3 = 8002
PORT_AUDIO = 8003
PORT_VIDEO4 = 8004
PORT_AUDIO2 = 8005

# 汎用映像受信関数（UDP）
def video_receiver(port, window_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, port))
    print(f"Receiving video on port {port}...")

    while True:
        try:
            data, _ = sock.recvfrom(65536)
            frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
            if frame is not None:
                cv2.imshow(window_name, frame)
            if cv2.waitKey(1) == ord('q'):
                break
        except Exception as e:
            print(f"{window_name} receive error: {e}")
            break

    sock.close()
    cv2.destroyWindow(window_name)

# 音声受信（TCP）
def audio_receiver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT_AUDIO))
    server_socket.listen(1)
    print("Waiting for audio connection...")
    conn, _ = server_socket.accept()
    print("Audio connection established.")

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

# 映像送信（UDP）
def video_sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cap = cv2.VideoCapture(0)
    print("Sending video to client...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        if len(buffer) < 65507:
            sock.sendto(buffer, (CLIENT_IP, PORT_VIDEO4))

    cap.release()
    sock.close()

# 音声送信（TCPクライアント）
def audio_sender():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Connecting to audio receiver on client...")
        client_socket.connect((CLIENT_IP, PORT_AUDIO2))
        print("Audio connection to client established.")
    except Exception as e:
        print(f"Audio send connect error: {e}")
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

# スレッド起動
threading.Thread(target=video_receiver, args=(PORT_VIDEO1, "Video1")).start()
threading.Thread(target=video_receiver, args=(PORT_VIDEO2, "Video2")).start()
threading.Thread(target=video_receiver, args=(PORT_VIDEO3, "Video3")).start()
threading.Thread(target=audio_receiver).start()
threading.Thread(target=video_sender).start()
threading.Thread(target=audio_sender).start()
