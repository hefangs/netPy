#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author  : he
@File    : test_api.py
@Date    : 2024/5/29 14:17
@Description: 
"""
import os
import time
import pytest
import requests
import yaml
from common.yaml_util import YamlUtil
from jsonpath_ng import parse
import re

@pytest.fixture(scope="class")
def clear():
    YamlUtil(os.getcwd() + "/extract.yaml").clear_yaml()
    print("数据已删除！！！")
    yield
    print("数据已生成！！！")

@pytest.mark.usefixtures("clear")
class TestLoginNet:
    @pytest.mark.parametrize("args", YamlUtil(os.getcwd() + "/testApi/test_generate_key.yaml").read_yaml())
    def test_generate_key(self, args):
        url = args["request"]["url"]
        res = requests.get(url)
        # print(res.json())
        response_json = res.json()
        extracted_data = {}
        # 提取数据 unikey
        if "extract" in args:
            extract_rules = args["extract"]
            for key, rule in extract_rules.items():
                jsonpath_expr = parse(rule)
                match = jsonpath_expr.find(response_json)
                if match:
                    extracted_data = {
                        'unikey': match[0].value
                    }
                    # 把 unikey 写入 extract.yaml 文件
        YamlUtil(os.getcwd() + "/extract.yaml").write_yaml(extracted_data)

    @pytest.mark.parametrize("args",YamlUtil(os.getcwd() + "/testApi/test_key_generate_qrcode.yaml").read_yaml())
    def test_key_generate_qrcode(self, args):
        # 800:过期  801:等待扫码  802:待确认  803:授权登录成功并返回cookies
        url = args["request"]["url"]
        params = args["request"]["params"]
        # 读取 extract.yaml 中的 unikey
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        unikey = extracted_data.get("unikey")
        # 替换 params 中的 ${extract(unikey)} 为实际的 unikey 值
        for key, value in params.items():
            if value == "${extract(unikey)}":
                params[key] = unikey
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_qrcode_check.yaml').read_yaml())
    def test_qrcode_check(self, args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 unikey
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        unikey = extracted_data.get("unikey")
        # 替换 params 中的 ${extract(unikey)} 为实际的 unikey 值
        for key, value in params.items():
            if value == "${extract(unikey)}":
                params[key] = unikey
        res = requests.get(url, params=params)
        # print(res.json())
        # 提取数据 cookie
        if "extract" in args:
            extract_rules = args["extract"]
            for key, rule in extract_rules.items():
                jsonpath_expr = parse(rule)
                match = jsonpath_expr.find(res.json())
                # print(match)
                if match:
                    # print('--------->',match[0].value)
                    value = re.search(r'([^;]+)', match[0].value)
                    if value:
                        # print('--------->',value.group(1))
                        extracted_data = { 
                            "cookie": value.group(1)
                        }
                        # 把cookie写入 extract.yaml 文件
        YamlUtil(os.getcwd() + "/extract.yaml").write_yaml(extracted_data)

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_send_captcha.yaml').read_yaml())
    def test_send_captcha(self,args):
        pass
    #     url = args['request']['url']
    #     params = args['request']['params']
    #     res = requests.get(url, params = params)
    #     print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_captcha_verify.yaml').read_yaml())
    def test_verify_captcha(self,args):
        pass
    #     url = args['request']['url']
    #     params = args['request']['params']
    #     captcha = input("请输入验证码：")
    #     params["captcha"] = captcha
    #     res = requests.get(url, params = params)
    #     print(res.json())
        
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_check_phone.yaml').read_yaml())
    def test_check_phone(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())
    
    def test_init_nickname(self):
        pass
    def test_check_nickname(self):
        pass
    def test_rebind_phone(self):
        pass
    def test_logout(self):
        pass
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_login_status.yaml').read_yaml())
    def test_login_status(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())
        # 提取数据 uid
        if "extract" in args:
            extract_rules = args["extract"]
            for key, rule in extract_rules.items():
                jsonpath_expr = parse(rule)
                match = jsonpath_expr.find(res.json())
                if match:
                    extracted_data = {
                        "uid": match[0].value
                    }
        YamlUtil(os.getcwd() + "/extract.yaml").write_yaml(extracted_data)           

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_detail.yaml').read_yaml())
    def test_user_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # print('---------->uid',id)
        # 替换 params 中的 ${extract(id)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
               params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_account.yaml').read_yaml())
    def test_user_account(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_subcount.yaml').read_yaml())
    def test_user_subcount(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_level.yaml').read_yaml())
    def test_user_level(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_binding.yaml').read_yaml())
    def test_user_binding(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # 替换 params 中的 ${extract(uid)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
                params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_update.yaml').read_yaml())
    def test_user_update(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res =requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_avatar_upload.yaml').read_yaml())
    def test_user_avatar_upload(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # headers = args['request']['headers']
        # # upload file
        # file_path = os.path.join(os.getcwd(), "test_avatar1.jpg")
        # print(file_path)
        # files = {'imgFile': open(file_path, 'rb')}
        # res = requests.post(url, params = params, headers = headers, files = files)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_pl_count.yaml').read_yaml())
    def test_user_pl_count(self,args):
        url = args['request']['url']
        res =requests.get(url)
        # print(res.text)

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_countries_code_list.yaml').read_yaml())
    def test_countries_code_list(self,args):
        url = args['request']['url']
        res =requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_playlist.yaml').read_yaml())
    def test_user_playlist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # 替换 params 中的 ${extract(uid)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
                params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_playlist_update.yaml').read_yaml())
    def test_user_playlist_update(self,args):
        pass
    #     url = args['request']['url']
    #     params = args['request']['params']
    #     res = requests.get(url, params = params)
    #     print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_playlist_name_update.yaml').read_yaml())
    def test_user_playlist_name_update(self,args):
        pass
    #     url = args['request']['url']
    #     params = args['request']['params']
    #     res = requests.get(url, params = params)
    #     print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_playlist_tag_update.yaml').read_yaml())
    def test_user_playlist_tag_update(self,args):\
        pass
    #     url = args['request']['url']
    #     params = args['request']['params']
    #     res = requests.get(url, params = params)
    #     print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_playlist_cover_update.yaml').read_yaml())
    def test_user_playlist_cover_update(self,args):
        pass
    #     url = args['request']['url']
    #     params = args['request']['params']

    #     res = requests.get(url, params = params)
    #     print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_comment_history.yaml').read_yaml())
    def test_user_comment_history(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # 替换 params 中的 ${extract(uid)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
                params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_dj.yaml').read_yaml())
    def test_user_dj(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # 替换 params 中的 ${extract(uid)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
                params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_follows.yaml').read_yaml())
    def test_user_follows(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # 替换 params 中的 ${extract(uid)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
                params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_followeds.yaml').read_yaml())
    def test_user_followeds(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # 替换 params 中的 ${extract(uid)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
                params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_event.yaml').read_yaml())
    def test_user_event(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # 替换 params 中的 ${extract(uid)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
                params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_record.yaml').read_yaml())
    def test_user_record(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 uid
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        uid = extracted_data.get("uid")
        # 替换 params 中的 ${extract(uid)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(uid)}"):
                params[key] = uid
        res = requests.get(url, params = params)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_hot_topic.yaml').read_yaml())
    def test_hot_topic(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())
        # 提取参数 actid
        if "extract" in args:
            extract_rules = args["extract"]
            for key, rule in extract_rules.items():
                jsonpath_expr = parse(rule)
                match = jsonpath_expr.find(res.json())
                if match:
                    extracted_data = {
                        'actid': match[0].value
                    }
                    # 把 unikey 写入 extract.yaml 文件
        YamlUtil(os.getcwd() + "/extract.yaml").write_yaml(extracted_data)

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_topic_detail.yaml').read_yaml())
    def test_topic_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 actId
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        actId = extracted_data.get("actid")
        # print('-------------------->',actId)
        # 替换 params 中的 ${extract(actId)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(actid)}"):
                params[key] = actId
                # print('------------->',params)
        res = requests.get(url, params = params)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_topic_detail_event_hot.yaml').read_yaml())
    def test_topic_detail_event_hot(self,args):
        url = args['request']['url']
        params = args['request']['params']
        # 读取 extract.yaml 中的 actId
        extracted_data = YamlUtil(os.getcwd() + "/extract.yaml").read_yaml()
        actId = extracted_data.get("actid")
        # print('-------------------->',actId)
        # 替换 params 中的 ${extract(actId)} 为实际的 id 值
        for key ,value in args["request"]["params"].items():
            if value == ("${extract(actid)}"):
                params[key] = actId
                # print('------------->',params)  
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_event.yaml').read_yaml())
    def test_event_list(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_list.yaml').read_yaml())
    def test_artist_list(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            "limit": params.get('limit','50'),
            "offset": params.get('offset','0'),
            "type": params.get('type','1'),
            "area": params.get('area','96'),
            "initial": params.get('initial','')
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_top_song.yaml').read_yaml())
    def test_artist_top_song(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_songs.yaml').read_yaml())
    def test_artist_songs(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            "id":params['id'],
            "order": params.get('order','hot'),
            "limit": params.get('limit','50'),
            "offset": params.get('offset','0'),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_sublist.yaml').read_yaml())
    def test_artist_sublist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            "limit": params.get('limit','50'),
            "offset": params.get('offset','0'),   
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_topic_sublist.yaml').read_yaml())
    def test_topic_sublist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            "limit": params.get('limit','10'),
            "offset": params.get('offset','1'),   
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mv_sublist.yaml').read_yaml())
    def test_mv_sublist(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_catlist.yaml').read_yaml())
    def test_playlist_catlist(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_hot.yaml').read_yaml())
    def test_playlist_hot(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_top_playlist.yaml').read_yaml())
    def test_top_playlist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            "order": params.get('order','hot'),
            "cat": params.get('cat','全部'),
            "limit": params.get('limit','50'),
            "offset": params.get('offset','0'),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_highquality_tags.yaml').read_yaml())
    def test_playlist_highquality_tags(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_top_playlist_highquality.yaml').read_yaml())
    def test_top_playlist_highquality(self,args):
        url = args['request']['url']
        params = args['request']['params']
        current_timestamp = int(time.time() * 1000)
        all_params = {
            "cat": params.get('cat','全部'),
            "limit": params.get('limit','50'),
            "before":params.get('before') or current_timestamp
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_related_playlist.yaml').read_yaml())
    def test_related_playlist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_detail.yaml').read_yaml())
    def test_playlist_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_track_all.yaml').read_yaml())
    def test_playlist_track_all(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            "id": params.get('id'),
            "limit": params.get('limit','50'),
            "offset": params.get('offset','0'),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_detail_dynamic.yaml').read_yaml())
    def test_playlist_detail_dynamic(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_update_playcount.yaml').read_yaml())
    def test_playlist_update_playcount(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_song_url.yaml').read_yaml())
    def test_song_url(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_song_url_v1.yaml').read_yaml())
    def test_song_url_v1(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_check_music.yaml').read_yaml())
    def test_check_music(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_search.yaml').read_yaml())
    def test_search(self,args):
        base_url = args['request']['base_url']
        endpoint = args['request']['endpoint']
        url = base_url + endpoint
        params = args['request']['params']
        if not params:
            res = requests.get(url)
        else:
          all_params = {
              "keywords": params['keywords'],
              "type": params.get('type','1'),
              "limit": params.get('limit','30'),
              "offset": params.get('offset','0'),
          }
          res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_create.yaml').read_yaml())
    def test_playlist_create(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_delete.yaml').read_yaml())
    def test_playlist_delete(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_subscribe.yaml').read_yaml())
    def test_playlist_subscribe(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        #  # 构建请求参数
        # all_params = {
        #     "id": params['id']
        # }
        #  # 添加必选参数 t（如果存在）
        # if 't' in params:
        #     all_params['t'] = params['t']
        # # 添加可选参数 limit 和 offset，并设置默认值
        # all_params['limit'] = params.get('limit',30)
        # all_params['offset'] = params.get('offset',1)
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_tracks.yaml').read_yaml())
    def test_playlist_tracks(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_track_add.yaml').read_yaml())
    def test_playlist_track_add(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_track_delete.yaml').read_yaml())
    def test_playlist_track_delete(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_video_recent.yaml').read_yaml())
    def test_playlist_video_recent(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_lyric.yaml').read_yaml())
    def test_lyric(self,args):
        base_url = args['request']['base_url']
        endpoint = args['request']['endpoint']
        params = args['request']['params']
        url = base_url + endpoint
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_top_song.yaml').read_yaml())
    def test_top_song(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_homepage_block_page.yaml').read_yaml())
    def test_homepage_block_page(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_homepage_dragon_ball.yaml').read_yaml())
    def test_homepage_dragon_ball(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())
  
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_music.yaml').read_yaml())
    def test_comment_music(self,args):
        url = args['request']['url']
        params = args['request']['params']
        times_tamp = int(time.time() * 1000)
        all_params = {
            'id': params['id'],
            'limit': params.get('limit', 20),
            'offset': params.get('offset', 0),
            'before': params.get('before', times_tamp),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_floor.yaml').read_yaml())
    def test_comment_floor(self,args):
        url = args['request']['url']
        params = args['request']['params']
        times_tamp = int(time.time() * 1000)
        all_params = {
            'parentCommentId': params['parentCommentId'],
            'id': params['id'],
            'type':params['type'],
            'limit': params.get('limit', 20),
            'time': params.get('time', times_tamp),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_album.yaml').read_yaml())
    def test_comment_album(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            'id': params['id'],
            'limit': params.get('limit', 20),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_playlist.yaml').read_yaml())
    def test_comment_playlist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time() * 1000)
        all_params = {
            'id': params['id'],
            'limit': params.get('limit', 20),
            'offset': params.get('offset', 0),
            'before': params.get('before', time_stamp),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_mv.yaml').read_yaml())
    def test_comment_mv(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time() * 1000)
        all_params = {
            'id': params['id'],
            'limit': params.get('limit', 20),
            'offset': params.get('offset', 0),
            'before': params.get('before', time_stamp),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_dj.yaml').read_yaml())
    def test_comment_dj(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time() * 1000)
        all_params = {
            'id': params['id'],
            'limit': params.get('limit', 20),
            'offset': params.get('offset', 0),
            'before': params.get('before', time_stamp),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_video.yaml').read_yaml())
    def test_comment_video(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time() * 1000)
        all_params = {
            'id': params['id'],
            'limit': params.get('limit', 20),
            'offset': params.get('offset', 0),
            'before': params.get('before', time_stamp),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_hot.yaml').read_yaml())
    def test_comment_hot(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time() * 1000)
        all_params = {
            'id': params['id'],
            'type': params['type'],
            'limit': params.get('limit', 20),
            'offset': params.get('offset', 0),
            'before': params.get('before', time_stamp),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_new.yaml').read_yaml())
    def test_comment_new(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time() * 1000)
        all_params = {
            'id': params['id'],
            'type': params['type'],
            'pageNo': params.get('pageNo', 1),
            'pageSize': params.get('pageSize', 20),
            'sortType': params.get('sortType', 3),
            'cursor': params.get('cursor', time_stamp),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_like.yaml').read_yaml())
    def test_comment_like(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_hug_comment.yaml').read_yaml())
    def test_hug_comment(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment_hug_list.yaml').read_yaml())
    def test_comment_hug_list(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'uid': params['uid'],
        #     'cid': params['cid'],
        #     'sid': params['sid'],
        #     'page': params.get('page', 20),
        #     'cursor': params.get('cursor', 20),
        #     'idCursor': params.get('idCursor', 20),
        #     'pageSize': params.get('pageSize', 0),
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_comment.yaml').read_yaml())
    def test_comment(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     't': params['t'],
        #     'type': params['type'],
        #     'id': params['id'],
        # }
        # if params['t'] == 1:
        #     all_params['content'] = params['content']
        # elif params['t'] == 2:
        #     all_params['commentId'] = params['commentId']
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_banner.yaml').read_yaml())  
    def test_banner(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_resource_like.yaml').read_yaml())  
    def test_resource_like(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())
  
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_mylike.yaml').read_yaml())  
    def test_playlist_mylike(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_song_detail.yaml').read_yaml())
    def test_song_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())
  
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album.yaml').read_yaml())
    def test_album(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_detail_dynamic.yaml').read_yaml())
    def test_album_detail_dynamic(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_sub.yaml').read_yaml())
    def test_album_sub(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_sublist.yaml').read_yaml())
    def test_album_sublist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            'limit': params.get('limit', 20),
            'offset': params.get('offset',1)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artists.yaml').read_yaml())
    def test_artists(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artists_mv.yaml').read_yaml())
    def test_artists_mv(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artists_album.yaml').read_yaml())
    def test_artists_album(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            'id':params['id'],
            'limit': params.get('limit', 20),
            'offset': params.get('offset',1)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artists_desc.yaml').read_yaml())
    def test_artists_desc(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artists_detail.yaml').read_yaml())
    def test_artists_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_simi_artist.yaml').read_yaml())
    def test_simi_artist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_simi_playlist.yaml').read_yaml())
    def test_simi_playlist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_simi_mv.yaml').read_yaml())
    def test_simi_mv(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())        

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_simi_song.yaml').read_yaml())
    def test_simi_song(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())        

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_simi_user.yaml').read_yaml())
    def test_simi_user(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())    

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_recommend_resource.yaml').read_yaml())
    def test_recommend_resource(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # print(res.json())    
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_recommend_songs.yaml').read_yaml())
    def test_recommend_songs(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # print(res.json())    

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_recommend_songs_dislike.yaml').read_yaml())
    def test_recommend_songs_dislike(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_history_recommend_songs.yaml').read_yaml())
    def test_history_recommend_songs(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json()

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_history_recommend_songs_detail.yaml').read_yaml())
    def test_history_recommend_songs_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_personal_fm.yaml').read_yaml())
    def test_personal_fm(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_daily_signin.yaml').read_yaml())
    def test_daily_signin(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_sign_happy_info.yaml').read_yaml())
    def test_sign_happy_info(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_like.yaml').read_yaml())
    def test_like(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_likelist.yaml').read_yaml())
    def test_likelist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_fm_trash.yaml').read_yaml())
    def test_fm_trash(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # res = requests.get(url, params = params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_top_album.yaml').read_yaml())
    def test_top_album(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
            'area': params.get('area', 'ZH'),
            'type': params.get('type', 'hot'),
            'year': params.get('year', 2024),
            'month': params.get('month', 6),
            'offset': params.get('offset', 0),
            'limit': params.get('limit', 30)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_new.yaml').read_yaml())
    def test_album_new(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'area': params.get('area', 'ZH'),
        #     'offset': params.get('offset', 0),
        #     'limit': params.get('limit', 30)
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())
        
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_newest.yaml').read_yaml())
    def test_album_newest(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_scrobble.yaml').read_yaml())
    def test_scrobble(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
          'sourceid': params['sourceid'],
          'time': params.get('time',291)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_top_artists.yaml').read_yaml())
    def test_top_artists(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',20),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mv_all.yaml').read_yaml())
    def test_mv_all(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'order': params.get('order','全部'),
          'area': params.get('area','全部'),
          'type': params.get('type','最热'),
          'limit': params.get('limit',20),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mv_first.yaml').read_yaml())
    def test_mv_first(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'area': params.get('area','全部'),
          'limit': params.get('limit',20),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mv_exclusive_rcmd.yaml').read_yaml())
    def test_mv_exclusive_rcmd(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',20),
          'offset': params.get('offset','0'),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_personalized_mv.yaml').read_yaml())
    def test_personalized_mv(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_personalized.yaml').read_yaml())
    def test_personalized(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit' : params.get('limit',20)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_personalized_newsong.yaml').read_yaml())
    def test_personalized_newsong(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit' : params.get('limit',10)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_personalized_djprogram.yaml').read_yaml())
    def test_personalized_djprogram(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_program_recommend.yaml').read_yaml())
    def test_program_recommend(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit' : params.get('limit',10),
          'offset' : params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_personalized_privatecontent.yaml').read_yaml())
    def test_personalized_privatecontent(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_personalized_privatecontent_list.yaml').read_yaml())
    def test_personalized_privatecontent_list(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',10),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_top_mv.yaml').read_yaml())
    def test_top_mv(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'area': params.get('area', '内地'),
          'limit': params.get('limit',10),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mv_detail.yaml').read_yaml())
    def test_mv_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'mvid': params.get('mvid', 1),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mv_detail_info.yaml').read_yaml())
    def test_mv_detail_info(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'mvid': params.get('mvid', 1),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mv_url.yaml').read_yaml())
    def test_mv_url(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
          'r': params.get('r', 1080),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_video_group_list.yaml').read_yaml())
    def test_video_group_list(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_video_category_list.yaml').read_yaml())
    def test_video_category_list(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_video_group.yaml').read_yaml())
    def test_video_group(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
          'offset': params.get('offset', 0),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_video_timeline_all.yaml').read_yaml())
    def test_video_timeline_all(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'offset': params.get('offset', 0),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_video_timeline_recommend.yaml').read_yaml())
    def test_video_timeline_recommend(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'offset': params.get('offset', 0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_related_allvideo.yaml').read_yaml())
    def test_related_allvideo(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_video_detail.yaml').read_yaml())
    def test_video_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_video_detail_info.yaml').read_yaml())
    def test_video_detail_info(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'vid': params['vid']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_video_url.yaml').read_yaml())
    def test_video_url(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_toplist.yaml').read_yaml())
    def test_toplist(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_toplist_detail.yaml').read_yaml())
    def test_toplist_detail(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_toplist_artist.yaml').read_yaml())
    def test_toplist_artist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'type': params.get('type', 1)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_cloud.yaml').read_yaml())
    def test_user_cloud(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'limit': params.get('limit', 1),
        #   'offset': params.get('offset', 1)
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_cloud_detail.yaml').read_yaml())
    def test_user_cloud_detail(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'id': params['id']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_cloud_del.yaml').read_yaml())
    def test_user_cloud_del(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'id': params['id']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_cloud_match.yaml').read_yaml())
    def test_cloud_match(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'uid': params['uid'],
        #   'sid': params['sid'],
        #   'asid': params['asid']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_banner.yaml').read_yaml())
    def test_dj_banner(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_personalize_recommend.yaml').read_yaml())
    def test_dj_personalize_recommend(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',5)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_subscriber.yaml').read_yaml())
    def test_dj_subscriber(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time())
        all_params = {
          'id': params['id'],
          'limit': params.get('limit',20),
          'time': params.get('time',time_stamp)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_user_audio.yaml').read_yaml())
    def test_user_audio(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'uid': params['uid'],
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_hot.yaml').read_yaml())
    def test_dj_hot(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_program_toplist.yaml').read_yaml())
    def test_dj_program_toplist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_toplist_pay.yaml').read_yaml())
    def test_dj_toplist_pay(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_program_toplist_hours.yaml').read_yaml())
    def test_dj_program_toplist_hours(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_toplist_hours.yaml').read_yaml())
    def test_dj_toplist_hours(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_toplist_newcomer.yaml').read_yaml())
    def test_dj_toplist_newcomer(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_toplist_popular.yaml').read_yaml())
    def test_dj_toplist_popular(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_toplist.yaml').read_yaml())
    def test_dj_toplist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30),
          'offset': params.get('offset',0),
          'type': params.get('type','hot')
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_radio_hot.yaml').read_yaml())
    def test_dj_radio_hot(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30),
          'offset': params.get('offset',0),
          'cateId': params.get('type', 2001)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_recommend.yaml').read_yaml())
    def test_dj_recommend(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_catelist.yaml').read_yaml())
    def test_dj_catelist(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_recommend_type.yaml').read_yaml())
    def test_dj_recommend_type(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'type': params['type']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_sub.yaml').read_yaml())
    def test_dj_sub(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'rid': params['rid']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_sublist.yaml').read_yaml())
    def test_dj_sublist(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_paygift.yaml').read_yaml())
    def test_dj_paygift(self,args):
        url = args['request']['url']
        param = args['request']['params']
        all_params = {
          'limit': param.get('limit',30),
          'offset': param.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_category_excludehot.yaml').read_yaml())
    def test_dj_category_excludehot(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_category_recommend.yaml').read_yaml())
    def test_dj_category_recommend(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_today_perfered.yaml').read_yaml())
    def test_dj_today_perfered(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_detail.yaml').read_yaml())
    def test_dj_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'rid': params['rid']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_program.yaml').read_yaml())
    def test_dj_program(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'rid': params['rid'],
          'limit': params.get('limit',30),
          'offset': params.get('offset',0),
          'asc': params.get('asc','false'),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_dj_program_detail.yaml').read_yaml())
    def test_dj_program_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_msg_private.yaml').read_yaml())
    def test_msg_private(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30),
          'offset': params.get('offset',30)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_send_text.yaml').read_yaml())
    def test_send_text(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'user_ids': params['user_ids'],
        #   'msg': params['msg']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_send_song.yaml').read_yaml())
    def test_send_song(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'user_ids': params['user_ids'],
        #   'msg': params['msg']
        #   'id': params['id']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_send_album.yaml').read_yaml())
    def test_send_album(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'user_ids': params['user_ids'],
        #   'msg': params['msg']
        #   'id': params['id']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_send_playlist.yaml').read_yaml())
    def test_send_playlist(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'user_ids': params['user_ids'],
        #   'msg': params['msg']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_msg_recentcontact.yaml').read_yaml())
    def test_msg_recentcontact(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_msg_private_history.yaml').read_yaml())
    def test_msg_private_history(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'uid':params['uid'],
          'limit':params.get('limit',30)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_msg_comments.yaml').read_yaml())
    def test_msg_comments(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'uid':params['uid'],
        #   'limit':params.get('limit',30)
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_msg_forwards.yaml').read_yaml())
    def test_msg_forwards(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'limit':params.get('limit',30),
        #   'offset':params.get('offset',30)
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_msg_notices.yaml').read_yaml())
    def test_msg_notices(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # time_stamp = int(time.time())
        # all_params = {
        #   'limit':params.get('limit',30),
        #   'lasttime':params.get('lasttime',time_stamp)
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_setting.yaml').read_yaml())
    def test_setting(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_list.yaml').read_yaml())
    def test_album_list(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',30),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_songsaleboard.yaml').read_yaml())
    def test_album_songsaleboard(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'albumType': params.get('albumType',1),
          'type': params.get('type','year'),
          'limit': params.get('limit',30),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_list_style.yaml').read_yaml())
    def test_album_list_style(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'area': params.get('area','Z_H'),
          'limit': params.get('limit',30),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_album_detail.yaml').read_yaml())
    def test_album_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_digitalAlbum_purchased.yaml').read_yaml())
    def test_digitalAlbum_purchased(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',10)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_digitalAlbum_ordering.yaml').read_yaml())
    def test_digitalAlbum_ordering(self,args):
        pass  
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'id': params['id'],
        #   'payment': params['payment'],
        #   'quantity': params['quantity']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_calendar.yaml').read_yaml())
    def test_calendar(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'startTime': params.get('startTime',0),
          'endTime': params.get('endTime',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei.yaml').read_yaml())
    def test_yunbei(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_today.yaml').read_yaml())
    def test_yunbei_today(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_sign.yaml').read_yaml())
    def test_yunbei_sign(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_info.yaml').read_yaml())
    def test_yunbei_info(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_tasks.yaml').read_yaml())
    def test_yunbei_tasks(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_tasks_todo.yaml').read_yaml())
    def test_yunbei_tasks_todo(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_task_finish.yaml').read_yaml())
    def test_yunbei_task_finish(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'userTaskId': params['userTaskId'],
        #   'depositCode': params.get('depositCode',0)
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_tasks_receipt.yaml').read_yaml())
    def test_yunbei_tasks_receipt(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',10),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_tasks_expense.yaml').read_yaml())
    def test_yunbei_tasks_expense(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',10),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_new_song.yaml').read_yaml())
    def test_artist_new_song(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time())
        all_params = {
          'limit': params.get('limit',10),
          'before': params.get('before',time_stamp)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_new_mv.yaml').read_yaml())
    def test_artist_new_mv(self,args):
        url = args['request']['url']
        params = args['request']['params']
        time_stamp = int(time.time())
        all_params = {
          'limit': params.get('limit',10),
          'before': params.get('before',time_stamp)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_rcmd_song.yaml').read_yaml())
    def test_yunbei_rcmd_song(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
          'reason': params.get('reason','test'),
          'yunbeiNum': params.get('yunbeiNum',1)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_yunbei_rcmd_song_history.yaml').read_yaml())
    def test_yunbei_rcmd_song_history(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'size': params.get('size',20),
          'cursor': params.get('cursor','')
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_song_purchased.yaml').read_yaml())
    def test_song_purchased(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',20),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mlog_url.yaml').read_yaml())
    def test_mlog_url(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mlog_to_video.yaml').read_yaml())
    def test_mlog_to_video(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_vip_growthpoint.yaml').read_yaml())
    def test_vip_growthpoint(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_vip_growthpoint_details.yaml').read_yaml())
    def test_vip_growthpoint_details(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',20),
          'offset': params.get('offset',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_vip_tasks.yaml').read_yaml())
    def test_vip_tasks(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_vip_growthpoint_get.yaml').read_yaml())
    def test_vip_growthpoint_get(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'ids': params['ids']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_fans.yaml').read_yaml())
    def test_artist_fans(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_follow_count.yaml').read_yaml())
    def test_artist_follow_count(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())
        
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_digitalAlbum_detail.yaml').read_yaml())
    def test_digitalAlbum_detail(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_digitalAlbum_sales.yaml').read_yaml())
    def test_digitalAlbum_sales(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'ids': params['ids']
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_musician_data_overview.yaml').read_yaml())
    def test_musician_data_overview(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_musician_play_trend.yaml').read_yaml())
    def test_musician_play_trend(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'startTime': params.get('startTime','2024-05-24'),
        #   'endTime': params.get('endTime','2024-05-30')
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_musician_tasks.yaml').read_yaml())
    def test_musician_tasks(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_musician_tasks_new.yaml').read_yaml())
    def test_musician_tasks_new(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_musician_cloudbean.yaml').read_yaml())
    def test_musician_cloudbean(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_musician_cloudbean_obtain.yaml').read_yaml())
    def test_musician_cloudbean_obtain(self,args):
         pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'id': params['id'],
        #   'period': params['period'],
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_vip_info.yaml').read_yaml())
    def test_vip_info(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_vip_info_v2.yaml').read_yaml())
    def test_vip_info_v2(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
        }
        res = requests.get(url, params = all_params)
        # print(res.json())
  
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_musician_sign.yaml').read_yaml())
    def test_musician_sign(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_mlog_music_rcmd.yaml').read_yaml())
    def test_mlog_music_rcmd(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'songid': params['songid'],
          'mvid': params.get('mvid',5343930),
          'limit': params.get('limit',10)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_playlist_privacy.yaml').read_yaml())
    def test_playlist_privacy(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #   'id': params['id'],
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_song_download_url.yaml').read_yaml())
    def test_song_download_url(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
          'br': params.get('br',320000)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_artist_video.yaml').read_yaml())
    def test_artist_video(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'id': params['id'],
          'size': params.get('size',10),
          'order': params.get('order',0),
          'cursor': params.get('cursor',0)
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_record_recent_song.yaml').read_yaml())
    def test_record_recent_song(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',100),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_record_recent_video.yaml').read_yaml())
    def test_record_recent_video(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',100),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_record_recent_voice.yaml').read_yaml())
    def test_record_recent_voice(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',100),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_record_recent_playlist.yaml').read_yaml())
    def test_record_recent_playlist(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',100),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_record_recent_album.yaml').read_yaml())
    def test_record_recent_album(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',100),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_record_recent_dj.yaml').read_yaml())
    def test_record_recent_dj(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'limit': params.get('limit',100),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_signin_progress.yaml').read_yaml())
    def test_signin_progress(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'moduleId': params.get('moduleId','1207signin-1207signin'),
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_inner_version.yaml').read_yaml())
    def test_inner_version(self,args):
        url = args['request']['url']
        res = requests.get(url)
        # print(res.json())
    
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_vip_timemachine.yaml').read_yaml())
    def test_vip_timemachine(self,args):
        url = args['request']['url']
        params = args['request']['params']
        all_params = {
          'startTime': params.get('startTime','1638288000000'),
          'endTime': params.get('endTime','1640966399999'),
          'limit': params.get('limit','60')
        }
        res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_song_wiki_summary.yaml').read_yaml())
    def test_song_wiki_summary(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'id': params['id']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())
        
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_sheet_list.yaml').read_yaml())
    def test_sheet_list(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'id': params['id']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())
        
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_sheet_preview.yaml').read_yaml())
    def test_sheet_preview(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'id': params['id']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())
        
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_style_list.yaml').read_yaml())
    def test_style_list(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'tagId': params['tagId']
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())
        
    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_style_preference.yaml').read_yaml())
    def test_style_preference(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_style_song.yaml').read_yaml())
    def test_style_song(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'tagId': params['tagId'],
        #     'cursor': params.get('cursor',0),
        #     'sort': params.get('sort',0)
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_style_album.yaml').read_yaml())
    def test_style_album(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'tagId': params['tagId'],
        #     'cursor': params.get('cursor',0),
        #     'size': params.get('size',20),
        #     'sort': params.get('sort',0)
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_style_playlist.yaml').read_yaml())
    def test_style_playlist(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'tagId': params['tagId'],
        #     'cursor': params.get('cursor',0),
        #     'size': params.get('size',20),
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_style_artist.yaml').read_yaml())
    def test_style_artist(self,args):
        pass
        # url = args['request']['url']
        # params = args['request']['params']
        # all_params = {
        #     'tagId': params['tagId'],
        #     'cursor': params.get('cursor',0),
        #     'size': params.get('size',20),
        # }
        # res = requests.get(url, params = all_params)
        # print(res.json())

    @pytest.mark.parametrize('args', YamlUtil(os.getcwd() + '/testApi/test_starpick_comment_rcmd.yaml').read_yaml())
    def test_starpick_comment_rcmd(self,args):
        pass
        # url = args['request']['url']
        # res = requests.get(url)
        # print(res.json())