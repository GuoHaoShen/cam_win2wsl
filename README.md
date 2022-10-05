# cam_win2wsl
 适用于wsl2到window的摄像头图像实时传输

目前WSL2 内核中暂时不包含 USB 摄像头驱动，无法使用opencv调用摄像头
为了解决这个问题，在window中用opencv读取摄像头，使用网络通信与wsl连通

## 本人测试环境：
window端
    python3.9.7
    opencv4.6.0

ubuntu20.04
    python3.8.10
    opencv4.6.0

## 使用方法

在window打开命令行，输入ipconfig查看本机IP地址
进入cam_wsl_client.py，将SERVER_ADDR变量中IP地址改为自己的的IP地址

window端运行cam_win_server.py

ubuntu端运行cam_wsl_client.py
