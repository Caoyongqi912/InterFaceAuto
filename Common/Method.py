# -*- coding: utf-8 -*-
# @Author  : caoyongqi
# @File    : Method.py
import os

import yaml
from Config import Config


class Method:
    """
    读取yml 整理
    """

    def __init__(self, filename, url):
        self.project_path = os.path.dirname(os.path.dirname(__file__))
        self.total_case_params = {}
        self.url = url
        self.domain = ''
        self.method = ''
        self.feature_name = ''
        self.story_name = ''
        self.test_case_list = {}
        self.init_param = ''

        self.test_case_parametrize_list = []

        # init domain
        self.config = Config.Config()

        # loading case
        self.load_case_list(filename, url)

        # case parametrize
        self.load_case_parametrize()

    def load_case_data_file(self, filename):
        """
        读取测试用例文件
        :param filename:
        :param url:
        :param method:
        :return:
        """
        case_data_path = os.path.join(os.path.join(self.project_path, 'CaseData'), filename)
        f = open(case_data_path, 'r')
        case_text = f.read()
        f.close()
        self.total_case_params = yaml.load(case_text)

    def load_case_list(self, filename, url):
        """
        整理测试用例文件, 区分method
        :param filename:
        :param url:
        :param method:
        :return:
        """
        self.load_case_data_file(filename)
        self.domain = self.config.domain
        for i in self.total_case_params['interface']:
            if i['url'] == url:
                self.method = i['method']
                self.url = url
                if 'story_name' in i:
                    self.story_name = i['story_name']
                if 'feature_name' in i:
                    self.feature_name = i['feature_name']

                self.test_case_list = i['test_case_list']
        if len(self.test_case_list) == 0:
            raise RuntimeError('case 加载失败')
        pass

    def load_case_parametrize(self):

        for k, v in self.test_case_list.items():
            v['case_name'] = k
            self.test_case_parametrize_list.append(v)
        self.test_case_parametrize_list.sort(key=lambda x: x['case_name'])


if __name__ == '__main__':
    param = Method('Comment_api.yml', '/review/v1/add')

    case_data_list = param.test_case_parametrize_list
    test_case_list = param.test_case_list
    domain = param.domain
    url = param.url
    method = param.method

    print(case_data_list)
