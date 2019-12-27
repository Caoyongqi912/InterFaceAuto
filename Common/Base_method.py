# -*- coding: utf-8 -*-
# @Time    : 2019/10/30
# @Author  : caoyongqi
# @Email   : v-caoyongqi@xiaomi.com
# @File    : Base_method.py
import json
import time

import requests
from Common import Log
from Config.Config import Config


class BaseMethod:
    HOST = Config().get_conf('domain', 'domain')
    log = Log.LogInfo()

    def add_comment(self, debug, appId, docId, title=None, url=None, documents='A', extra=None, location=None,
                    requestId=None, videosInfo=None):
        """
        增加評論
        """
        Data = {}
        Data['appId'] = appId
        Data['debug'] = debug
        Data['docId'] = docId
        Data['documents'] = documents
        Data['extra'] = extra
        Data['title'] = title
        Data['location'] = location
        Data['requestId'] = requestId
        Data['videosInfo'] = videosInfo
        Data['url'] = url
        res = json.loads(requests.post(url=self.HOST + "/review/v1/add", data=Data).text)
        time.sleep(1)
        if res['status'] != 0:
            self.log.error(f'   ======== 增加评论失败: {res["desc"]} ========')
        else:
            self.log.debug(f'   ======== 增加一条评论: {res["data"]} ========')
            return res['data']

    def add_replyComment(self, reviewId, appId, docId, debug, requestId=None):
        """
        回复评论
        """
        data = {}
        data['appId'] = appId
        data['docId'] = docId
        data['debug'] = debug
        data['documents'] = 'A'
        data['reviewId'] = reviewId
        data['requestId'] = requestId

        res = json.loads(requests.post(url=self.HOST + "/review/v1/add", data=data).text)
        time.sleep(1)

        if res['status'] != 0:

            self.log.error(f'   ======== 对{reviewId}回复失败 ======== \n   ======== 错误原因: {res["desc"]} ========')

        else:
            self.log.debug(f'   ======== 对{reviewId}回复成功 ======== \n   ======== 返回ID: {res["data"]} ========')
            return res['data']

    def delete_comment(self, appId, reviewId, docId, debug):
        """
        刪除評論
        """
        data = {}
        data['appId'] = appId
        data['reviewId'] = reviewId
        data['docId'] = docId
        data['debug'] = debug

        res = json.loads(requests.post(url=self.HOST + "/review/v1/delete", data=data).text)
        time.sleep(1)

        if res['status'] == 0:
            self.log.debug(f'   ========= 删除评论: {reviewId} ========')
        else:
            self.log.error(f'   ========= 删除失败: {res["desc"]} ========')

    def support_comment(self, support, docId, appId, reviewId, debug):
        """
        點贊
        """
        data = {}
        data['support'] = support
        data['docId'] = docId
        data['appId'] = appId
        data['reviewId'] = reviewId
        data['debug'] = debug

        res = json.loads(requests.post(url=self.HOST + '/review/v1/support', data=data).text)
        time.sleep(1)

        if res['status'] == 0:
            if support is True:
                self.log.debug(f'   ======== 對{reviewId}点赞成功! ========')
            else:
                self.log.debug(f'   ======== 對{reviewId}取消点赞! ========')
        else:
            self.log.error(f'   ======== 對{reviewId}点赞失败! ======== \n    ======== 失败原因:{res["desc"]} ========')

    def add_irrigation_review(self, userId, appId, docId, reviewId=None, userName='tester', title=None, url=None,
                              documents='A', extra=None,
                              location=None,
                              requestId=None, videosInfo=None, needAudit=None):
        """
        增加一条灌水评论
        """
        data = {}
        data['appId'] = appId
        data['docId'] = docId
        data['documents'] = documents
        data['userName'] = userName
        data['userSign'] = self.get_userSign(data['appId'])
        data['reviewId'] = reviewId
        data['userId'] = userId
        data['title'] = title
        data['url'] = url
        data['requestId'] = requestId
        data['extra'] = extra
        data['location'] = location
        data['videosInfo'] = videosInfo
        data['needAudit'] = needAudit
        res = json.loads(requests.post(url=self.HOST + "/review/admin/add", data=data).text)
        time.sleep(1)

        if res['status'] != 0:
            self.log.error(f'    ======== 增加灌水评论失败: {res["desc"]} ========')
        else:
            self.log.debug(f'    ======== 增加一条灌水评论: {res["data"]} ========')
            return res['data']['reviewId']

    def get_userSign(self, appId):
        """
        获取userSign
        :param appId:
        :return:
        """
        data = {'appId': appId}
        res = requests.get(url=self.HOST + "/test/userSign", params=data)
        time.sleep(1)

        # print(res.text)
        return res.text

    def get_userSign_Uid(self, appId, uId):

        data = {}
        data['uid'] = uId
        data['appKey'] = self.get_userSign(appId)
        res = requests.get(url=self.HOST + "/test/userSign", params=data)
        time.sleep(1)

        return res.text

    def get_userSign_AppKey_Uid_AppId(self, appID, uid):
        key = self.get_userSign(appId=appID)
        data = {}
        data['uid'] = uid
        data['appKey'] = key
        data['appId'] = appID
        res = requests.get(url=self.HOST + "/test/userSign", params=data)
        time.sleep(1)

        return res.text


if __name__ == '__main__':
    documents1 = '顾志强陪同蒋建国深入嘉荫县青山乡上马村检查指导工作'
    documents2 = '顾志强陪同蒋建国深入石家庄市无极县检查指导工作'
    docu3 = '顾志强陪同蒋建国深入大连市甘井子区检查指导工作'
    userSign = BaseMethod().get_userSign('browser')
    print(userSign)
    local = '{"longitude": 100.0, "latitude": 12.0, "country": "中国", "province": "北京", "city": "北京", "district": "海淀区","street": "安宁庄东路", "streetNum": "7号", "address": "北京海淀区安宁庄东路蜂巢工厂"}'
    reviewID = BaseMethod().add_comment(debug=189, docId=19, appId='bikan', location=local, documents=documents2,
        title="News", url='https://www.xiaomi.com')
    # BaseMethod().delete_comment(appId='bikan', reviewId='6f:18:9223370463905106809:4187', docId=18, debug=189)
    # time.sleep(1)
    # BaseMethod().support_comment(support=True, docId=18, appId='bikan', reviewId=reviewID, debug=200)
    # time.sleep(0.5)
    # BaseMethod().add_replyComment(appId="bikan", docId=18, debug=200,)
    # BaseMethod().add_irrigation_review(appId='bikan',docId=18,userId=189)
    # print(BaseMethod().get_userSign_Uid("bikan",'189'))
    # print(BaseMethod().get_userSign(appId='bikan'))
    # BaseMethod().add_replyComment(reviewId=reviewID, appId='bikan', docId=18, debug=189)
    BaseMethod().add_irrigation_review(userId=189, docId=19, appId='bikan', location=local, documents=documents2,
                                     title="News", url='https://www.xiaomi.com', needAudit=False)
    dd =BaseMethod().get_userSign_AppKey_Uid_AppId(appID='bikan',uid=189)
    print(dd)