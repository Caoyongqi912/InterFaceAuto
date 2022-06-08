

import os
import yaml
import random
import jsonpath
import Config.Config as Config

class CaseInit:
    def __init__(self, filename, url=None):
        self.project_path = os.path.dirname(os.path.dirname(__file__))
        self.url = url
        self.host = ''
        self.method = ''
        self.feature_name = ''
        self.story_name = ''
        self.total_case = {}
        self.test_case_list = {}
        self.confest_case_list = {}
        self.config = Config.Config()

        self.load_case_yaml_file(filename)

        if url:
            # load case
            self.load_case_list(url)
            # get real vale
            self.get_real_value()

    def load_case_yaml_file(self, filename):
        """
        读取测试用例yaml文件
        :param filename:
        :return:
        """
        case_file_path = os.path.join(os.path.join(self.project_path, 'Params'), filename)
        # f = open(case_file_path, 'r')
        # case_text = f.read()
        with open(case_file_path,'r',encoding='UTF-8') as f:
            case_text = f.read()
        f.close()
        self.total_case = yaml.load(case_text)
        if filename =='conftest_api.yml':
            self.confest_case_list = self.total_case['confest']

    def load_case_list(self, url):
        """
        整理测试用例文件
        :param filename:
        :param url:
        :return:
        """
        self.host = self.config.host
        self.feature_name = self.total_case['feature_name']

        for api in self.total_case['interface']:
            if api['url'] == url:
                self.url = url
                self.method = api['method']
                self.story_name = api['story_name']
                self.test_case_list = api['test_case_list']
        if len(self.test_case_list) == 0:
            raise RuntimeError('case 加载失败')
        self.test_case_list.sort(key=lambda x: x['case_name'])
        pass

    def get_real_value(self):
        '''
        替换用例参数中的真实值,将值为item.替换成实际值
        :return:
        '''
        for case in self.test_case_list:
            for step in case['teststeps']:
                # appid更新为配置文件中的默认值
                if step['requests'] and 'appId' in step['requests']:
                    step['requests']['appId'] = self.config.appId
                if step['url'] == 'item.url':
                    step['url'] = self.url
                if step['method'] == 'item.method':
                    step['method'] = self.method

class ReplaceVale:

    def replace_conftest(self, case_step, confest_dict):
        '''
        替换.yml参数中用到conftest函数值的参数，同时也适用于替换conftest.yml中需要上一个请求返回值
        :param case_step:
        :param confest_function
        :param extract_value:
        :return:
        '''
        if case_step['requests']:
            for key, value in case_step['requests'].items():
                # 判断requests中需要替换conftest值的字段
                if isinstance(value, dict) and 'conftest' in value.keys():
                    if value['conftest'] not in confest_dict.keys():
                        raise Exception('replace conftest error: conftest not exist')
                    case_step['requests'][key] = confest_dict[value['conftest']]
        if case_step['body']:
            self.replace_other_conftest(case_step['body'], confest_dict)
        if 'jsonpath' in case_step.keys() and case_step['jsonpath']:
            self.replace_other_conftest(case_step['jsonpath'], confest_dict)

    def replace_other_conftest(self, data, confest_dict):
        '''
        替换body和jsonpath参数中需要用到conftest函数值的参数
        :param data:
        :param confest_dict:
        :return:
        '''
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and 'conftest' not in value.keys():
                    self.replace_other_conftest(value, confest_dict)
                elif isinstance(value, dict) and 'conftest' in value.keys():
                    if value['conftest'] not in confest_dict.keys():
                        raise Exception('replace conftest error: conftest not exist')
                    else:
                        data[key] = confest_dict[value['conftest']]
                elif isinstance(value, list):
                    for index in range(0, len(value)):
                        # 这种类型的数据 "aids": [{'conftest': 'boardId'}]
                        if isinstance(value[index], dict) and 'conftest' not in value[index].keys():
                            self.replace_other_conftest(value[index], confest_dict)
                        elif isinstance(value[index], dict) and 'conftest' in value[index].keys():
                            if value[index]['conftest'] not in confest_dict.keys():
                                raise Exception('replace conftest error: conftest not exist')
                            else:
                                value[index] = confest_dict[value[index]['conftest']]
                        elif isinstance(value[index], list):
                            self.replace_other_conftest(value[index], confest_dict)
        elif isinstance(data, list):
            for its in data:
                self.replace_other_conftest(its, confest_dict)

    def replace_extract(self, case_step, extract_list):
        '''
        替换参数中需要从上一步返回值中提取的值
        :param case_step:
        :param extract_value:
        :return:
        '''
        if case_step['requests']:
            for key, value in case_step['requests'].items():
                # requests中value一旦是字典类型，肯定是需要extract，根据step_name,在extract_list中找对应的值
                if isinstance(value, dict):
                    case_step['requests'][key] = extract_list[value['step_name']][value['extract']]
                    if value['step_name'] not in extract_list.keys():
                        raise Exception('replace extract error: step_name not exist')
        if case_step['body']:
            self.replace_other_extract(case_step['body'], extract_list)
        if 'jsonpath' in case_step.keys() and case_step['jsonpath']:
            self.replace_other_extract(case_step['jsonpath'], extract_list)


    def replace_other_extract(self, data, extract_list):
        '''
        替换body和jsonpath参数中需要从上一步返回值中提取的值
        :param case_step:
        :param extract_value:
        :return:
        '''
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and 'extract' not in value.keys():
                    self.replace_other_extract(value, extract_list)
                elif isinstance(value, dict) and 'extract' in value.keys():
                    if value['step_name'] not in extract_list.keys():
                        raise Exception('replace extract error: step_name not exist')
                    else:
                        data[key] = extract_list[value['step_name']][value['extract']]
                elif isinstance(value, list):
                    for index in range(0, len(value)):
                        # 这种类型的数据 "aids": [{'step_name': 'step_01_creat_parentboard', 'extract': entity}]
                        if isinstance(value[index], dict) and 'extract' not in value[index].keys():
                            self.replace_other_extract(value[index], extract_list)
                        elif isinstance(value[index], dict) and 'extract' in value[index].keys():
                            if value[index]['step_name'] not in extract_list.keys():
                                raise Exception('replace extract error: step_name not exist')
                            else:
                                value[index] = extract_list[value[index]['step_name']][value[index]['extract']]
                        elif isinstance(value[index], list):
                            self.replace_other_extract(value[index], extract_list)
        elif isinstance(data, list):
            for its in data:
                self.replace_other_extract(its, extract_list)

    def get_extract(self, case_step, body_data, response_data, extract_list):
        '''
        获取每个casestep需要提取的extract值，保存在字典中
        :param case_step:
        :param data:
        :param extract_list: eg. {'step_01_XXX':{'entity': 11111}}
        :return:
        '''
        if case_step['extract']:
            extract_value = {}
            for key, value in case_step['extract'].items():
                # 判断提取的值是否在body中，如果是：extract: {'body':{'boardName':'$.boardName'}}
                if key == 'body':
                    for key, value in case_step['extract']['body'].items():
                        extract_value[key] = jsonpath.jsonpath(body_data, value)[0]
                        extract_list[case_step['name']] = extract_value
                else:
                    extract_value[key] = jsonpath.jsonpath(response_data, value)[0]
                    extract_list[case_step['name']] = extract_value
            return extract_list


    def replace_random(self, case_step):
        '''
        替换参数中需要随机生成值
        :param case_step:
        :return:
        '''
        # 替换requests中的值
        if case_step['requests']:
            for key, value in case_step['requests'].items():
                if isinstance(value, str) and 'random' in value:
                    case_step['requests'][key] = self.random_value(value)

        # 替换body中的值
        if case_step['body']:
            self.replace_body_random(case_step['body'])

    def replace_body_random(self, body):
        '''
        替换body中需要随机生成值
        :param body:
        :return:
        '''
        if isinstance(body, dict):
            for key, value in body.items():
                if isinstance(value, str) and 'random' in value:
                    body[key] = self.random_value(value)
                elif isinstance(value, dict):
                    self.replace_body_random(value)
                elif isinstance(value, list):
                    for its in value:
                        self.replace_body_random(its)
        elif isinstance(body, list):
            for its in body:
                self.replace_body_random(its)

    def random_value(self, random_type):
        '''
        生成随机字符串
        :param random_type: 随机值类型
        :return:
        '''
        # 字符串
        if random_type == 'random.string':
            return '自动化' + str(random.randint(1, 100000000))
        # 整型
        elif random_type == 'random.int':
            return random.randint(1, 10000000000)

