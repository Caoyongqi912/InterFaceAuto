# # -*- coding: utf-8 -*-
# # @Time    : 2019/8/29
#
#
# import json
# import os
# import sys
# import time
#
# import allure
# import pytest
#
# sys.path.append(os.getcwd())
# from Config.Method import CaseInit, ReplaceVale
# from Common.Request import Request
# from Common.Assert import Assertion
# from Common.Shell import Shell
# from Common.Log import LogInfo
#
# log = LogInfo()
#
#
# class TestAnnounceAddComplexAnnounce:
#     interface_name = '/api/get'
#     test_case_info = CaseInit('admin_api.yml', interface_name)
#     replace_value = ReplaceVale()
#
#     # case参数
#     feature = test_case_info.feature_name
#     story = test_case_info.story_name
#     host = test_case_info.host
#     url = test_case_info.url
#     test_case_list = test_case_info.test_case_list
#     extract_list = {}
#
#     @classmethod
#     def setup_class(cls):
#         log.info("==== 接口：%s ====" % '/announce/addComplexAnnounce')
#
#     @allure.feature(feature)
#     @allure.story(story)
#     @pytest.mark.parametrize('case_list_param', test_case_list)
#     @pytest.mark.flaky(reruns=2, reruns_delay=2)
#     def test_case(self, case_list_param):
#         log.info("=== title：%s ===" % case_list_param['case_name'])
#
#         case_name = case_list_param['case_name']
#         description = case_list_param['description']
#         test_steps = case_list_param['teststeps']
#
#         allure.dynamic.title(case_name)
#         allure.dynamic.description(description)
#
#         for index in range(len(test_steps)):
#             log.info("=== step：%s ===" % test_steps[index]['des'])
#             self.run_step(test_steps[index]['des'], test_steps[index])
#
#     @allure.step("步骤 {1}")
#     def run_step(self, case_step_des, case_step, conftest_function=None):
#         '''
#         执行测试步骤
#         :param case_step:
#         :param confest_function:要执行的conftest函数
#         :return:
#         '''
#
#         # 验证的case需要等待
#         if "sleep" in case_step['name']:
#             time.sleep(2)
#
#         # 替换需要随机数作为数值的变量
#         self.replace_value.replace_random(case_step)
#         # 用confest值替换变量值
#         self.replace_value.replace_conftest(case_step, conftest_function)
#         # 替换需要从上一步结果中提取的变量值
#         self.replace_value.replace_extract(case_step, self.extract_list)
#
#         try:
#             response = Request().requests(case_step['method'], case_step['url'], case_step['requests'],
#                                           case_step['body'], case_step['headers'])
#         except Exception as e:
#             log.error(e)
#             pytest.fail(str(e), pytrace=False)
#         else:
#             response_data = json.loads(str(response.text), encoding="utf-8")
#
#             allure.attach(self.host, 'host')
#             allure.attach(case_step['url'], 'url')
#             allure.attach(case_step['method'], 'method')
#             allure.attach(json.dumps(case_step['requests']), 'Params')
#             allure.attach(json.dumps(case_step['body']), 'body')
#             allure.attach(json.dumps(case_step['headers']), 'headers')
#             allure.attach(json.dumps(case_step['jsonpath']), 'jsonPath校验')
#             allure.attach(json.dumps(case_step['response'], ensure_ascii=False), '期望结果',
#                           allure.attachment_type.JSON)
#             allure.attach(json.dumps(response_data, ensure_ascii=False), '实际结果', allure.attachment_type.JSON)
#
#             Assertion().assert_code(response.status_code, 200)
#             Assertion().assert_key_value(response_data, case_step['response'])
#             Assertion().assert_jsonpath(response_data, case_step['response'], case_step['jsonpath'])
#
#             # 提取需要从结果中保存的字段
#             self.replace_value.get_extract(case_step, case_step['body'], response_data, self.extract_list)
#
#     @classmethod
#     def teardown_class(cls):
#         log.info("==== 接口用例执行完成 ====")
#
#
# if __name__ == "__main__":
#     shell = Shell()
#     report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Report')
#     xml_report_path = os.path.join(report_path, 'CommunitySystemTestXml')
#     html_report_path = os.path.join(report_path, 'CommunitySystemTestHtml')
#     if os.path.exists(xml_report_path):
#         shell.invoke('rm -r %s' % xml_report_path)
#     pytest.main(['-s', '-q', 'test_announceAddComplexAnnounce.py', '--alluredir', xml_report_path])
#
#     if os.path.exists(html_report_path):
#         shell.invoke('rm -r %s' % html_report_path)
#     cmd = 'allure generate %s -o %s --clean' % (xml_report_path, html_report_path)
#     try:
#         shell.invoke(cmd)
#     except Exception:
#         log.error('执行用例失败，请检查环境配置')
#         raise
