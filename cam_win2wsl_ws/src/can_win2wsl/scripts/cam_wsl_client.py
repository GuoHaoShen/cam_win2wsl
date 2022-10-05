from socket import *
import json, time, select, sys
import cv2
import numpy as np
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Image
from cv_bridge import CvBridge , CvBridgeError

BUFF_LEN     = 400                   # 最大报文长度
SERVER_ADDR  = ("172.16.19.207", 18000)  # 指明服务端地址,需要改为自己的IP地址

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

    rospy.init_node('camera_node', anonymous=True) #定义节点
    image_pub=rospy.Publisher('image_raw', Image, queue_size = 1) #定义话题

    # 创建 UDP Socket
    UDP_socket = socket(AF_INET, SOCK_DGRAM)
    # 设置socket超时时间，单位：秒
    UDP_socket.settimeout(2)

    # 检查是否连接成功
    check_link()

    timeStart = 0
    while not rospy.is_shutdown():
        data = None
        try:
            ready = select.select([UDP_socket], [], [], 0.1)
            if ready[0]:
                data, _ = UDP_socket.recvfrom(921600)
            #print("recv data succcess!")
            receive_data = np.frombuffer(data, dtype='uint8')
            img = cv2.imdecode(receive_data, 1)

            try:
                print("fps of recv data: ",1.0/(time.time()-timeStart))
            except Exception as e:
                print(e)
                time.sleep(0.2)
            timeStart = time.time()

            cv2.putText(img, "client", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('client', img)

            ros_frame = Image() 
            header = Header(stamp = rospy.Time.now())
            header.frame_id = "Camera"
            ros_frame.header=header
            ros_frame.width = 640
            ros_frame.height = 480
            ros_frame.encoding = "bgr8"
            ros_frame.step = 1920
            ros_frame.data = np.array(img).tostring() #图片格式转换
            image_pub.publish(ros_frame) #发布消息

        except Exception as e:
            print(e)
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    UDP_socket.close()
    cv2.destroyAllWindows()
    print("quit successfully!")