from socket import *
import json, time, select, sys
from tabnanny import check
import cv2
import numpy as np


def check_link():
    '''检查是否连接成功'''
    try_times = 0
    while try_times<20:
        try_times += 1
        UDP_socket.sendto(f'服务端UDP发送了信息'.encode(), SERVER_ADDR)
        #print('发送UDP数据成功')
        try:
            print('wait for server,times:',try_times)
            ready = select.select([UDP_socket], [], [], 0.1)
            if ready[0]:
                #print("尝试接受数据")
                data, client_addr = UDP_socket.recvfrom(921600)
            if data:
                print("link success!")
                break
        except:
            time.sleep(0.2)
            continue
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    if try_times>=20:
        print("The connection timed out. Please start again")
        sys.exit()

if __name__ == '__main__':
    BUFF_LEN     = 400                   # 最大报文长度
    SERVER_ADDR  = ("172.18.195.59", 18000)  # 指明服务端地址

    # 创建 UDP Socket
    UDP_socket = socket(AF_INET, SOCK_DGRAM)
    # 设置socket超时时间，单位：秒
    UDP_socket.settimeout(2)

    # 检查是否连接成功
    check_link()

    timeStart = 0
    while True:
        data = None
        try:
            ready = select.select([UDP_socket], [], [], 0.1)
            if ready[0]:
                data, _ = UDP_socket.recvfrom(921600)
            #print("recv data succcess!")
            receive_data = np.frombuffer(data, dtype='uint8')
            r_img = cv2.imdecode(receive_data, 1)

            try:
                print("fps of recv data: ",1.0/(time.time()-timeStart))
            except Exception as e:
                print(e)
                time.sleep(0.2)
            timeStart = time.time()

            cv2.putText(r_img, "client", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('client', r_img)

        except Exception as e:
            print(e)
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    UDP_socket.close()
    cv2.destroyAllWindows()