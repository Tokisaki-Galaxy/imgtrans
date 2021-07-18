# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import base64
import hashlib
import json
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox

from imp import reload

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/ocrtransapi'
APP_KEY = '6c5ae627b9bc7449'
APP_SECRET = 'kjYPXgaZT7kZ8eT5r1bccf6Y4lPHJpEU'

def analysejson(fpath,strbase):
    sdata = json.loads(strbase)
    #print(base64.b64decode(sdata['render_image']))
    with open(fpath, 'wb') as f: # 二进制方式打开图文件
        f.write(base64.b64decode(sdata['render_image']))
    

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.md5()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(fpath):
    f = open(fpath, 'rb')  # 二进制方式打开图文件
    q = base64.b64encode(f.read()).decode('utf-8')  # 读取文件内容，转换为base64编码
    f.close()

    data = {}
    data['from'] = 'auto'
    data['to'] = 'en'
    data['type'] = '1'
    data['q'] = q
    salt = str(uuid.uuid1())
    signStr = APP_KEY + q + salt + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['salt'] = salt
    data['sign'] = sign
    data['render'] = '1'

    response = do_request(data)
    #print(response.content)
    analysejson(fpath,response.content)

if __name__ == '__main__':

    tar_path = []
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory() #获得选择好的文件夹

    os.chdir(folder_path)
    s_name = os.listdir()
    for i in range(len(s_name)):
        tar_path.append(os.getcwd()+'\\'+s_name[i])
    
    for i in range(len(tar_path)):
            connect(tar_path[i])
    tkinter.messagebox.showinfo('提示','转换完成')