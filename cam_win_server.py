from socket import *
import json , time, select, sys
import cv2
import numpy as np

def check_link():
    '''检查是否连接成功'''
    try_times = 0
    while try_times<20:
        try_times += 1
        try:
            print('wait for client,times: ',try_times)
            #data, client_addr = UDP_socket.recvfrom(921600)
            ready = select.select([UDP_socket], [], [], 0.1)
            if ready[0]:
                #print("尝试接受数据")
                data, client_addr = UDP_socket.recvfrom(921600)

            for i in range(10):
                str_data = bytes('send'.encode())
                UDP_socket.sendto(str_data, client_addr)
                time.sleep(0.1)

            print("link success!")
            break
        except Exception as e :
            print(e)
            time.sleep(0.2)
            continue
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    if try_times>=20:
        print("The connection timed out. Please start again")
        sys.exit()
    return client_addr

if __name__ == '__main__':

    # 读取摄像头---------------------
    cap = cv2.VideoCapture(0)

    BUFF_LEN = 400    # 最大报文长度
    ADDR     = ("", 18000)  # 指明服务端地址，IP地址为空表示本机所有IP

    # 创建 UDP Socket
    UDP_socket = socket(AF_INET, SOCK_DGRAM)
    # 绑定地址
    UDP_socket.bind(ADDR)

    # 检查是否有连接
    CLIENT_ADDR = check_link()  #等待有客户端连入并报存IP地址

    timeStart = 0
    while True:
        _, img = cap.read()

        img = cv2.flip(img, 1)
        # 压缩图片
        _, send_data = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])
        #print("send_data : ",send_data)

        UDP_socket.sendto(send_data, CLIENT_ADDR)
        #print(f'正在发送数据，大小:{img.nbytes} Byte')

        try:
            print("fps of send data: ",1.0/(time.time()-timeStart))
        except Exception as e:
            print(e)
            time.sleep(0.2)
        timeStart = time.time()

        cv2.putText(img, "server", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('server', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break