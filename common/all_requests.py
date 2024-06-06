#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author  : he
@File    : all_requests.py.py
@Date    : 2024/5/31 23:45
@Description: 
"""
import json

import requests


class AllRequests:
    session = requests.Session()

    @staticmethod
    def all_sent_request(self, method, url, data, **kwargs):
        print("--------------------------")
        method = str(method).lower()
        res = None
        if method == 'get':
            res = AllRequests.session.request(method=method, url=url, params=data, **kwargs)
        elif method == 'post':
            strdata = json.dumps(data)
            res = AllRequests.session.request(method=method, url=url, data=strdata, **kwargs)
        else:
            print('不支持的请求方式')
        return res
