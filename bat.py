import sys
import uuid
import editor.upload_cos
import editor.createdzi
import os
import time
from natsort import natsorted
from PIL import Image
from mysql_data.mysqlContent import SQL
import urllib3
from urllib import request
from urllib.parse import quote
import string
import socket
import shutil
import logging
from logging import handlers



class MainCode():
    logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                        filename='running.log',
                        filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        # 日志格式
                        )
    def __init__(self,tablename):
        logger = logging.getLogger()
        handler = logging.FileHandler('running.log')
        logger.handlers.append(handler)
        # self.doing(self);
        sql = SQL()
        #设置表名
        #tablename = 'cy_standard_jewel_content'
        data_list = sql.selectall(tablename)
        lenth = len(data_list)
        if(lenth>0):
            for each in data_list:
                # 清空temp文件夹
                shutil.rmtree('temp')
                os.mkdir('temp')
                url = each['file_url']
                url = quote(url, safe=string.printable)
                path = self.download_url(url)
                if (path):
                    # 创建dzi切片
                    dzi_path = editor.createdzi.createImg(path)
                    if(dzi_path):
                        # 上传dzi
                        dzi_url = editor.upload_cos.upload_dzi(dzi_path)
                        if (dzi_url):
                            result = sql.setdzi(tablename, dzi_url, each['id'])
                            print(result)


    # 下载文件
    def download_url(self,image_url):
        #image_name = os.path.basename(image_url)
        suffix = os.path.splitext(image_url)[-1]
        file_name = 'dzi' + str(uuid.uuid1()).replace('-','') + suffix
        # 设置超时时间为30s
        socket.setdefaulttimeout(30)
        # 解决下载不完全问题且避免陷入死循环
        try:
            request.urlretrieve(image_url, 'temp/'+file_name)
            return 'temp/' + file_name
        except socket.timeout:
            count = 1
            while count <= 5:
                try:
                    request.urlretrieve(image_url, 'temp/'+image_name)
                    return 'temp/'+file_name
                    break
                except socket.timeout:
                    err_info = '下载图片：Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                    logging.exception(err_info)
                    count += 1
            if count > 5:
                logging.exception('图片下载失败')
                return False


if __name__ == '__main__':
    while 1:
        MainCode('cy_standard_jewel_content')
        #MainCode('cy_standard_user_content')
        # 延时60秒
        logging.info('running......')
        time.sleep(60)