# -*- coding: utf-8 -*-
# @Time    : 2019/9/23
# @Author  : caoyongqi
# @Email   : v-caoyongqi@xiaomi.com
# @File    : main.py
import os
import sys
import pytest
from Common import Log
from Common.Shell import Shell
from Config.Config import Config

BASEPATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    log = Log.LogInfo()
    conf = Config()
    shell = Shell()
    # 初始化报告路径
    case_path = ''
    if len(sys.argv) == 4:
        # 自动化执行时，控制台传入报告路径与测试域名
        xml_report_path = os.path.join(sys.argv[1])
        test_host = os.path.join(sys.argv[2])
        # 初始化config文件
        conf.set_conf('domain', 'domain', test_host)
        if sys.argv[-1] == "true":
            case_path = 'TestCase/Admin'
        else:
            case_path = 'TestCase/Other'


    else:
        # 本地执行

        xml_report_path = conf.xml_report_path

    # 用例执行
    args = ['-s', '-q', case_path, '--alluredir', xml_report_path]
    pytest.main(args=args)

    # 本地执行需要加以下几行->生成allure报告
    # html_report_path = conf.html_report_path
    # if os.path.exists(html_report_path):
    #     shell.invoke('rm -r %s' % html_report_path)
    # cmd = 'allure generate %s -o %s --clean' % (xml_report_path, html_report_path)
    # try:
    #     shell.invoke(cmd)
    # except Exception:
    #     log.error('执行用例失败，请检查环境配置')
    #     raise
