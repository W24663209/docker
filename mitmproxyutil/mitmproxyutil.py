# -*- coding: utf-8 -*-

from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
import logging
import lxml

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='mitmproxyutil.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    # format=
                    # '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )
'''
抓包工具
'''


class Addon(object):

    def request(self, flow):
        # do something in response
        pass

    def response(self, flow):
        if flow.request.url.__contains__('webchat.7moor.com'):
            print(flow.request.url)
            # with open('1.html','r') as f:
            # flow.response.text=f.read()
            # with open('1.json','r') as f:
            flow.response.text = ''
        allow_headers = flow.response.headers.get('Access-Control-Allow-Headers')  # type: str
        accept = flow.request.headers.get('Accept')  # type: str
        # if not flow.request.url.__contains__('192.168.1.131'):
        #     return
        if not ((allow_headers and allow_headers.__contains__('X-Requested-With')) or (
                accept and accept.__contains__('application/json'))):
            return
        if flow.response.text:
            query = {}
            url = flow.request.url
            method = flow.request.method
            text = flow.response.text
            request_query = flow.request.query
            if not request_query:
                query = flow.request.text
            for key in request_query:
                query[key] = request_query.get(key)
            # print('请求地址:%s\n请求方式:%s\n请求信息:%s\n返回信息:%s' % (url, method, query, text))
            logging.info('请求地址:%s\n请求方式:%s\n请求信息:%s\n返回信息:%s' % (url, method, query, text))
            print('请求地址:%s\n请求方式:%s\n请求信息:%s\n返回信息:%s' % (url, method, query, text))
            print('\n')
    # do something in response


class ProxyMaster(DumpMaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        try:
            DumpMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()


if __name__ == "__main__":
    options = Options(listen_host='0.0.0.0', listen_port=8080, http2=True)
    config = ProxyConfig(options)
    master = ProxyMaster(options, with_termlog=False, with_dumper=False)
    master.server = ProxyServer(config)
    master.addons.add(Addon())
    master.run()
