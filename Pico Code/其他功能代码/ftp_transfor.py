# -*- coding:utf-8 -*-
from ftplib import FTP
import os

#设置FTP连接信息
address= '******'
port= 21
user_name= '******'
password= '******'

#本地要上传的文件名
local_file_name="/media/******"
all_files = []

#FTP中要下载的文件名
remote_file_name="/******"
all_files_ftp = []

def get_all_files(filepath):
    files = os.listdir(filepath)
    for file1 in files:
        path1 = os.path.join(filepath,file1)
        if os.path.isdir(path1):
            get_all_files(path1)
        else:
            all_files.append(path1)
get_all_files(local_file_name)


#将文件上传到FTP
def upload_file(local_file_name):

    try:
        ftp = FTP()
        ftp.connect(address,port)
        ftp.login(user_name,password)
        remote_path="/Projects/12_Fruits_Recognization/01_data/01_Original_data"#如：将本地文件上传到FTP目录
        ftp.cwd(remote_path)
        num1 = len(all_files)
        for i in range(num1):
            path1 = all_files[i]
            (name1,extension1) = os.path.split(path1)
            (name2,extension2) = os.path.split(name1)
            ####如果有两级目录文件夹####
            # (name3,extension3) = os.path.split(name2)#如果有两级目录文件夹
            # new_path2 = os.path.join(remote_path,extension3,extension2)
            # if extension3 not in ftp.nlst(remote_path):
            #     ftp.mkd(new_path2)
            #########################
            new_path1 = os.path.join(remote_path,extension2)
            if new_path1 not in ftp.nlst(remote_path):
                ftp.mkd(new_path1)
            ftp.cwd(new_path1)
            file=open(path1,'rb')
            ftp.set_pasv(0)    
            ftp.storbinary('STOR %s' % os.path.basename(path1),file)    
            file.close()    
        ftp.close()
        print("文件上传完成")
    except Exception as e:
        print("文件上传失败...")
        print(str(e))



#从FTP中下载文件到本地,测试通过一级文件目录与直接下载
def download_file(remote_file_name):

    ftp = FTP()  
    ftp.connect(address, port)
    ftp.login(user_name,password)
    ftp.set_pasv(0)

    def get_all_ftp_files(path1):
        files1 = ftp.nlst(path1)
        for file1 in files1:
            if len(ftp.nlst(file1)) > 1:
                get_all_ftp_files(file1)
            elif len(ftp.nlst(file1)) == 0:
                print("Null file!!!")
            else:
                all_files_ftp.append(file1)

    get_all_ftp_files(remote_file_name)
    (name1,extension1) = os.path.split(remote_file_name)

    try:
        #设置FTP上文件下载到本地的位置
        local_path="/media/pico/data/FTP_data/"
        num1 = len(all_files_ftp)
        for i in range(num1):
            print(all_files_ftp[i])
            file_name1 = all_files_ftp[i].split('/')[-2]
            if file_name1 != extension1:
                new_path1 = os.path.join(local_path,file_name1)
                if not os.path.exists(new_path1):
                    os.makedirs(new_path1)

                local_file_name=os.path.join(new_path1,os.path.basename(all_files_ftp[i]))              
                file = open(local_file_name, 'wb')
                #从FTP服务器下载文件到前一步创建的文件对象，其中写对象为file.write，1024是缓冲区大小  
                ftp.retrbinary('RETR '+all_files_ftp[i],file.write,1024)   
                file.close() 
            else:
                local_file_name=local_path + os.path.basename(all_files_ftp[i])
                file = open(local_file_name, 'wb')
                ftp.retrbinary('RETR '+all_files_ftp[i],file.write,1024)  
                file.close() 
        print("文件下载完成")

    except Exception as e:
        print("文件上传失败...")
        print(str(e))
    ftp.close()


if __name__ == '__main__':

    #upload_file(local_file_name)
    #download_file(remote_file_name)