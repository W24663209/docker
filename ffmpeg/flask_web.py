#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   flask_web.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/6/17 4:13 下午   gxrao      1.0         None
'''

# import lib
from flask import Flask, request
import os, time, uuid, oss2, sys
from bson import json_util

management = Flask(__name__)

# 文件地址
file_path = "source/"
# 文件输出地址
file_out_path = "out/"


@management.route('/compression_video', methods=["GET"])
def compression_video():
    file_name = file_path + request.args['fileName']
    out_file_name = file_out_path + str(uuid.uuid4()) + '.mp4'
    start_time = time.time()
    try:
        shell = 'cd %s;ffmpeg -y -i %s.mp4 -c:v libx265 -b:v 1024k -x265-params pass=1 -an -f mp4 /dev/null && ffmpeg -i %s.mp4 -c:v libx265 -b:v 1024k -x265-params pass=2 -c:a copy %s' % (
            sys.path[0], file_name, file_name, out_file_name)
        print(shell)
        os.system(shell)
        eng_time = time.time()
        print("耗时:%s秒" % (eng_time - start_time))
    except:
        return json_util.dumps("解压失败")
    try:
        return json_util.dumps(upload(sys.path[0] + "/" + out_file_name, out_file_name))
    except:
        with open('error/error.txt', 'a') as f:
            f.write(out_file_name)
        return json_util.dumps("上传失败,文件路径:%s" % (out_file_name))


def upload(fileNamePath, fileName):
    '''
    上传选中图片
    :param fileNamePath: 本地图片地址
    :param text:要复制的url
    :return:
    '''
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth('LTAIaA3Wsl58RyAd', 'u8pJ53qlZ4iY8d9Yt4ritbasWbxa5Q')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    # 服务器地址
    host = 'https://oss-cn-shenzhen.aliyuncs.com'
    # 存储空间名称
    yourBucketName = 'weizongtang-file'

    bucket = oss2.Bucket(auth, host, yourBucketName)
    # 要保存的目录
    save_dir = 'upload'
    # 生成的网络图片名称
    bucket.put_object_from_file('%s/%s' % (save_dir, fileName), fileNamePath)
    # 生成适应markdown的图片地址
    # ![WechatIMG1163](/Users/weizongtang/Pictures/WechatIMG1163.jpeg)
    # https://weizongtang-img.oss-cn-shenzhen.aliyuncs.com/myblog/54783bcc-1fe3-11ea-93f5-80fa5b59c6ef.png
    network_url = 'https://%s.oss-cn-shenzhen.aliyuncs.com/%s/%s' % (yourBucketName, save_dir, fileName)
    return network_url


if __name__ == '__main__':
    management.run(host='0.0.0.0', port=9999)
