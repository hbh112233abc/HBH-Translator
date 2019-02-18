#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'huangbinghe@gmail.com'

from urllib import parse, request
import re
import hashlib
import random
import json


class BaiduTranslate():
    def __init__(self, appid, secret_key):
        self.appid = appid
        self.secret_key = secret_key
        self.api = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.__from_lang = 'auto'
        self.__to_lang = 'zh'
        self.q = ''

    @property
    def from_lang(self):
        '''get from language'''
        return self.__from_lang

    @from_lang.setter
    def from_lang(self, lang='auto'):
        '''set from language'''
        self.__from_lang = lang

    @property
    def to_lang(self):
        '''get to language'''
        return self.__to_lang

    @to_lang.setter
    def to_lang(self, lang='zh'):
        '''set to language'''
        self.__to_lang = lang

    def __make_sign(self):
        '''create sign, return salt,sign'''
        salt = str(random.randint(32768, 65536))
        print('salt:', salt)
        sign = self.appid+self.q+salt+self.secret_key
        print('before sign:', sign)
        m1 = hashlib.md5()
        m1.update(bytes(sign, encoding='utf8'))
        sign = m1.hexdigest()
        print('sign:', sign)
        return salt, sign

    def __make_params(self):
        '''create params'''

        salt, sign = self.__make_sign()
        params = {
            'appid': self.appid,
            'q': self.q,
            'from': self.__from_lang,
            'to': self.__to_lang,
            'salt': salt,
            'sign': sign
        }
        print('params:', params)
        params = parse.urlencode(params).encode('utf-8')
        print('params urlencode:', params)
        return params

    def query(self, q):
        '''wait translate string:q'''
        self.q = q

        params = self.__make_params()
        try:
            req = request.Request(self.api, data=params)
            r = request.urlopen(req).read().decode('utf-8')
            print('baidu api response:', r)
            r = json.loads(r)
            error_code = r.get('error_code', '52000')
            if error_code != '52000':
                return self.error(error_code)

            result = r.get('trans_result', [])
            if len(result) < 1:
                raise Exception('tanslate fail')
            dst = []
            for x in result:
                dst.append(x.get('dst', ''))
            print('dst:', dst)
            dst_str = ' '.join(dst)
            return dst_str
        except Exception as e:
            print('error:', str(e))
        finally:
            pass

    def error(self, code=''):
        '''get error message'''
        error_msg = {
            '52000': 'success',
            '52001': 'request timeout,try again',
            '52002': 'system error,try again',
            '52003': 'unauth user,please check your appid or secret_key',
            '54000': 'params empty',
            '54001': 'sign error',
            '54003': 'Access frequency constraints',
            '54004': 'balance is not enough',
            '54005': 'Frequent long query,wait 3 second then try again',
            '58000': 'client IP error',
            '58001': 'language not support',
            '58002': 'service close'
        }

        return error_msg.get(code, '未知错误')

    def to_cn(self, q):
        self.__to_lang = 'zh'
        return self.query(q)

    def to_en(self, q):
        self.__to_lang = 'en'
        return self.query(q)


if __name__ == '__main__':
    appid = '20190214000266737'
    secret_key = 'Nf7QSdPjC1Zf_VHSo_r9'
    t = BaiduTranslate(appid, secret_key)
    res = t.query('apple is a good phone')
    print(res)
