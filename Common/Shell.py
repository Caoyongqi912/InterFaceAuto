# -*- coding: utf-8 -*-
# @Time    : 2019/10/11
# @Author  : caoyongqi
# @Email   : v-caoyongqi@xiaomi.com
# @File    : Shell.py

"""
封装执行shell语句方法

"""

import subprocess


class Shell:
    @staticmethod
    def invoke(cmd):
        print("执行命令：", cmd)
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(output)
        print(errors)
        o = output.decode("utf-8")
        return o
