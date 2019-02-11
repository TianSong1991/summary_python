# -*- coding:utf-8 -*-

from urlparse import urlparse
import datetime
import base64
import hmac
import hashlib
import json
import urllib2
import shutil
import os
import time

ak_id = '******'
ak_secret = '******'


def get_json(image_path):
    def get_current_date():
        date = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
        return date
    def to_md5_base64(strBody):
        hash = hashlib.md5()
        hash.update(body)
        return hash.digest().encode('base64').strip()
    def to_sha1_base64(stringToSign, secret):
        hmacsha1 = hmac.new(secret, stringToSign, hashlib.sha1)
        return base64.b64encode(hmacsha1.digest())
    options = {
        'url': 'https://dtplus-cn-shanghai.data.aliyuncs.com/face/attribute',
        'method': 'POST',
        'body': json.dumps({"type": "1","content":base64.b64encode((open(image_path,'rb')).read())}, separators=(',', ':')),
        'headers': {
            'accept': 'application/json',
            'content-type': 'application/json',
            'date':  get_current_date(),
            'authorization': ''
        }
    }

    body = ''
    if 'body' in options:
        body = options['body']
        
    bodymd5 = ''
    if not body == '':
        bodymd5 = to_md5_base64(body)

    urlPath = urlparse(options['url'])
    if urlPath.query != '':
        urlPath = urlPath.path + "?" + urlPath.query
    else:
        urlPath = urlPath.path
    stringToSign = options['method'] + '\n' + options['headers']['accept'] + '\n' + bodymd5 + '\n' + options['headers']['content-type'] + '\n' + options['headers']['date'] + '\n' + urlPath
    signature = to_sha1_base64(stringToSign, ak_secret)

    authHeader = 'Dataplus ' + ak_id + ':' + signature
    options['headers']['authorization'] = authHeader

    request = None
    method = options['method']
    url = options['url']

    if 'GET' == method or 'DELETE' == method:
        request = urllib2.Request(url)
    elif 'POST' == method or 'PUT' == method:
        request = urllib2.Request(url, body)
    request.get_method = lambda: method
    for key, value in options['headers'].items():
        request.add_header(key, value)
    try:
        conn = urllib2.urlopen(request)
        response = conn.read()
        print(response)

        txt_name=image_path+".json"
        fh = open(txt_name, 'w')
        fh.write(response)
        fh.close()


    except urllib2.HTTPError, e:
        print e.read()
        raise SystemExit(e)


def move_files(movepath,rootpath,notmovepath):
    movefiles1 = os.listdir(rootpath)
    for file1 in movefiles1:
        path1 = os.path.join(rootpath,file1)
        movefiles2 = os.listdir(path1)
        for file2 in movefiles2:
            (name1,extension1) = os.path.splitext(file2)
            path2 = os.path.join(path1,file2)
            if extension1 == '.json':
                h_file=open(path2,'r')
                age_json_string=h_file.read()
                h_file.close()
                age_json=json.JSONDecoder().decode(age_json_string)
                if 'age' in age_json:
                    age1 = age_json['age'][0]
                    movepath1 = os.path.join(movepath,str(age1))
                    if not os.path.exists(movepath1):
                        os.makedirs(movepath1)
                    path3 = os.path.join(path1,name1)
                    print(path3)
                    shutil.copy(path3,movepath1)
                else:
                    path3 = os.path.join(path1,name1)
                    if not os.path.exists(notmovepath):
                        os.makedirs(notmovepath)
                    shutil.copy(path3,notmovepath)
                    



if __name__ == '__main__':
    
    root_path = 'I:\\face_recognition\\age_1\\1Kevin'#人工错误挑选图片文件夹，路径最好使用英文，如果使用中文前面加u。

    files_list = os.listdir(root_path)

    move_path = 'I:\\face_recognition\\age_1\\aliyun'#阿里云分类文件夹，路径最好使用英文，如果使用中文前面加u。
    
    not_movepath = 'I:\\face_recognition\\age_1\\not_aliyun'#阿里云识别不出图片分类文件夹，路径最好使用英文，如果使用中文前面加u。
    
    for file1 in files_list:
        path1 = os.path.join(root_path,file1)
        files_list1 = os.listdir(path1)
        for file2 in files_list1:
            path2 = os.path.join(path1,file2)
            (name1,extension1) = os.path.splitext(file2)
            if extension1 == '.json':
                continue
            get_json(path2)
            time.sleep(2)
            
    move_files(move_path,root_path,not_movepath)