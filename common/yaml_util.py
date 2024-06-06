#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author  : he
@File    : yaml_util.py
@Date    : 2024/5/29 17:34
@Description: 
"""
import os

import yaml


class YamlUtil:
    def __init__(self, yaml_file):
        # 通过init方法把yaml文件传入这个类
        self.yaml_file = yaml_file

    def read_yaml(self):
        # 读取yaml文件，反序列化
        with open(self.yaml_file, encoding="utf-8") as f:
            value = yaml.load(f, Loader=yaml.FullLoader)
            # print(value)
            return value

    def write_yaml(self, data):
        with open(self.yaml_file, mode="a", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)

    def clear_yaml(self):
        with open(self.yaml_file, encoding="utf-8", mode="w") as f:
            f.truncate()
    # def read_yaml():
    #     with open(os.getcwd() + '/test_generate_key.yaml', encoding="utf-8") as f:
    #         value = yaml.load(stream=f, Loader=yaml.FullLoader)
    #         return value
    #
    # def write_yaml(data):
    #     with open(os.getcwd() + '/test_generate_key.yaml', encoding="utf-8", mode="a") as f:
    #         yaml.dump(data, stream=f, allow_unicode=True)
    #
    # def clear_yaml():
    #     with open(os.getcwd() + '/test_generate_key.yaml', encoding="utf-8", mode="w") as f:
    #         f.truncate()
