#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-4-26 上午11:09


from hashlib import sha1

def sha_name(s: str):
    sha_name = sha1(s.encode(encoding='utf-8')).hexdigest()
    return sha_name
