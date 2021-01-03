import os
import time
from PIL import Image

import paramiko  # 用于调用scp命令
from scp import SCPClient

cloth_path = ''
def ssh_scp_put(ip, username, password, local_file, remote_path):

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=str(ip), port=22, username=username, password=password)

    scp = SCPClient(ssh.get_transport())
    scp.put(local_file, recursive=True, remote_path=remote_path)
    scp.close()


def remote_scp(host_ip, remote_path, local_path, username, password):
    try:
        t = paramiko.Transport((host_ip, 22))
        t.connect(username=username, password=password) # 登录远程服务器
        sftp = paramiko.SFTPClient.from_transport(t) # sftp传输协议
        src = remote_path
        des = local_path
        sftp.get(src, des) #下载文件
        t.close()
        return True
        
    except IOError as e:
        return False

def main():
    print("trying on")
    global num
    ip = "10.110.210.24"
    username = "ypd-24-2"
    password = "ypd-24-2"

    local_up1 = "./data/test/cloth/004325_1.jpg"
    remote_up1 = "/home/ypd-24-2/DownLoad/cp-vton/data/test/cloth/004325_1.jpg"
    local_up2 = "./data/test/image/000010_0.jpg"
    remote_up2 = "/home/ypd-24-2/DownLoad/cp-vton/data/test/image/000010_0.jpg"
    local_down = "./data/test/tom_final.pth/test/try-on/result.jpg"
    remote_down = "/home/ypd-24-2/DownLoad/cp-vton/data/test/tom_final.pth/test/try-on/result.jpg"

    num = 0  # 不显示服务器上原始空result图像
    rootdir = "/home/pi/Downloads/"  # 树莓派蓝牙文件夹 提前随便存一个文件
    #rootdir = r"C:\Users\73916\Desktop\aaaa"
    while True:
        time.sleep(1)
        list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        print(len(list))
        if len(list) == 2:
            for i in range(2):
                path = os.path.join(rootdir, list[i])
                file = os.path.splitext(path)
                filename, type = file
                if type == ".jpg":
                    cloth_path = path
                    print(path)
                    if(os.path.getsize(cloth_path)!=0):
                        #break
                        cloth_file = Image.open(cloth_path)
                        print(cloth_file.size)
                        x_s = 192
                        y_s = 256
                        #x_s = 300
                        #y_s = 400
                        cloth_out = cloth_file.resize((x_s, y_s), Image.ANTIALIAS)
                        cloth_out.save('./data/test/cloth/004325_1.jpg')
                        print(cloth_out.size)
                        os.remove(cloth_path)
                        break

        a = os.path.exists(local_up1)
        b = os.path.exists(local_up2)
        if (a):
            if (b):
                #image_file = Image.open('/media/pi/F4AE-07BC/cp-vton/body.jpg')
                image_file = Image.open('./data/test/image/000010_0.jpg')
                x_s = 192
                y_s = 256
                image_out = image_file.resize((x_s, y_s), Image.ANTIALIAS)
                image_out.save('./data/test/image/000010_0.jpg')
                #image_out.save('/media/pi/F4AE-07BC/cp-vton/data/test/image/000010_0.jpg')
                #             image_file = Image.open('./data/test/image/000010_0.jpg')
                #             image_out = image_file.resize((x_s,y_s),Image.ANTIALIAS)
                #             image_out.save('./data/test/image/000010_0.jpg')
                #             print(image_out.size)
                # 更改image大小 ->(192,256)
                ssh_scp_put(ip, username, password, local_up1, remote_up1)
                print("finished up")
                ssh_scp_put(ip, username, password, local_up2, remote_up2)
                os.remove(local_up1)
                os.remove(local_up2)
                num = 0
                #print(num)
        if (num == 0):
            #print(num)
            #a = remote_scp(ip, remote_down, local_down, username, password)
            #print(a)
            if ((remote_scp(ip, remote_down, local_down, username, password))):
                num = 1
                print("finished down")
                star_file = Image.open("./data/test/tom_final.pth/test/try-on/result.jpg")
                print(star_file.size)
                star_width = 192*2
                star_height = 256*2
                star_out = star_file.resize((300, 400), Image.ANTIALIAS)
                star_out.save("./data/test/tom_final.pth/test/try-on/result.jpg")
                return 1



if __name__ == '__main__':
    main()