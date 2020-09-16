# -*- coding: utf-8 -*-
# @Author  : caoyongqi
# @File    : Request.py
import json
import requests
import requests.adapters as ad
from Common import Log

log = Log.LogInfo()


class Request:
    def __init__(self):
        ad.DEFAULT_RETRIES = 5
        s = requests.sessions
        s.keep_alive = False

    def requests(self, method, host, url, data, case_name, description,headers=None, files=None):

        log.debug('')
        log.debug('')
        log.debug('=== request_functions ===')
        log.debug(f"case_name   {case_name}")
        log.debug(f"des         {description}")
        log.debug(f"method      {method}")
        log.debug(f"host        {host}")
        log.debug(f"url         {url}")
        log.debug(f"data        {data}")
        log.debug(f"files       {files}")
        log.debug(f"headers     {headers}")

        if method == 'POST':
            try:
                self.response = requests.post(url=host + url, data=data, headers=headers,
                                              files=files)
                log.debug(f'res         {self.response.text}')
            except Exception as e:
                log.error(str(e))
                log.error(f'res         {self.response.text}')
                log.error('Post 请求异常')

        elif method == "GET":
            try:
                self.response = requests.get(url=host + url, params=data, headers=headers, files=files)
                log.debug(f'res         {self.response.text}')

            except Exception as e:
                log.error(str(e))
                log.error(f'res         {self.response.text}')
                log.error('Post 请求异常')

        Response = {}
        Response['status_code'] = self.response.status_code
        if Response['status_code'] == 500:
            Response['text'] = None
        elif self.response.text:
            Response['text'] = json.loads(self.response.text)
        else:
            Response['text'] = None
        return Response


if __name__ == '__main__':
    Request().requests(method='POST', host='http://staging.comment.inf.miui.srv/api/comment',
                       url='/review/admin/add',
                       data={'appId': 'bikan', 'documents': '6f:18:9223370464341342533:1422', 'docId': 18,
                             'userName': 'tester'},
                       description='dd', case_name='dd')
