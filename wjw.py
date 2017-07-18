# -*- coding: UTF-8 -*-
# author: zhuangshq
# email: 1120692265@qq,com
# This is a crawler for SYSU wjw system.
# It's easy to understand the code.
# This program contains five functions.
# get_payload:
# get_url_1
# get_url_2
# get_cookie
# get_grade(username, password, year, term): all the params are typed string
import json, urllib
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')


global JSESSIONID


def get_payload(username, password):
    global JSESSIONID
    payload = {}
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.8",
        'connection': "keep-alive",
        'host': "cas.sysu.edu.cn",
        'referer': "http://wjw.sysu.edu.cn/",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'upgrade-insecure-requests': "1",
        }
    url = 'https://cas.sysu.edu.cn/cas/login?service=http://uems.sysu.edu.cn/jwxt/casLogin?_tocasurl=http://wjw.sysu.edu.cn/cas'
    response = requests.request("GET", url, headers=headers)
    JSESSIONID = ''
    for item in response.cookies:
        if item.name == 'JSESSIONID':
            JSESSIONID = item.value
    LT = re.search(r'name="lt" value="(.*)" />', response.text).group(1)
    execution = re.search(r'name="execution" value="(.*)" />', response.text).group(1)
    payload['username'] = username
    payload['password'] = password
    payload['lt'] = LT
    payload['execution'] = execution
    payload['_eventId'] = 'submit'
    payload['submit'] = '登录'
    return payload


def get_url_1(username, password):
    payload = get_payload(username, password)
    payload = urllib.urlencode(payload)
    global JSESSIONID
    url = "https://cas.sysu.edu.cn/cas/login;jsessionid=%s?service=http://uems.sysu.edu.cn/jwxt/casLogin?_tocasurl=http://wjw.sysu.edu.cn/cas" % JSESSIONID
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.8",
        'connection': "keep-alive",
        'host': "cas.sysu.edu.cn",
        'referer': "https://cas.sysu.edu.cn/cas/login?service=http://uems.sysu.edu.cn/jwxt/casLogin?_tocasurl=http://wjw.sysu.edu.cn/cas",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'cookie': 'JSESSIONID=%s' % JSESSIONID,
        'origin': "https://cas.sysu.edu.cn",
        'upgrade-insecure-requests': "1",
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "max-age=0",
        'Content-Length': "%d" % len(payload)
        }
    response = requests.request("POST", url, data=payload, headers=headers, allow_redirects=False)
    # TGC = ''
    # CASPRIVACY = ''
    # for item in response.cookies:
    #     if item.name == 'TGC':
    #         TGC = item.value
    url = response.headers['Location']
    return url


def get_url_2(username, password):
    global JSESSIONID
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8",
        'connection': "keep-alive",
        'host': "uems.sysu.edu.cn",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'upgrade-insecure-requests': "1",
        'cache-control': "max-age=0",
        }
    url = get_url_1(username, password)
    response = requests.request("GET", url, headers=headers, allow_redirects=False)
    for item in response.cookies:
        if item.name == 'JSESSIONID':
            JSESSIONID = item.value
    url = response.headers['Location']
    headers['Cookie'] = "JSESSIONID=%s" % JSESSIONID
    response = requests.request("GET", url, headers=headers, allow_redirects=False)
    url = response.headers['Location']
    sno = url[67:75]        # get j_username
    jpasswd = url[87:]      # get j_password
    response = requests.request("GET", url, headers=headers, allow_redirects=False)
    url = response.headers['Location']
    response = requests.request("GET", url, headers=headers, allow_redirects=False)
    # begin to get the info of student
    url = "http://wjw.sysu.edu.cn/cas?REALSESSIONID=%s&XH=%s&MU=" % (JSESSIONID, sno)
    return url


def get_cookie(username, password):
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8",
        'connection': "keep-alive",
        'host': "wjw.sysu.edu.cn",
        'referer': "http://uems.sysu.edu.cn/jwxt/login.do?method=login",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'upgrade-insecure-requests': "1",
        }
    url = get_url_2(username, password)
    response = requests.request("GET", url, headers=headers, allow_redirects=False)
    return response.cookies



def get_grade(username, password, year, term):
    url = "http://wjw.sysu.edu.cn/api/score?year=%s&term=%s&pylb=01" % (year, term)
    headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8",
        'connection': "keep-alive",
        'host': "wjw.sysu.edu.cn",
        'referer': "http://wjw.sysu.edu.cn/score",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest'
        }
    cookie = get_cookie(username, password)
    response = requests.request("GET", url, headers=headers, allow_redirects=False, cookies=cookie)
    data = response.text
    data = re.search(r'\[(.*)\]', data)
    data = json.loads(data.group())     # transform str to array
    # print data
    grades = []
    for i in data:
        grade = {}
        grade['课程名称'] = i['kcmc']
        grade['教师'] = i['jsxm']
        grade['学分'] = i['xf']
        grade['绩点'] = i['jd']
        grade['排名'] = i['njzypm']
        # print "课程名称：%s 教师：%s 学分：%s 绩点：%s 排名：%s" % (i['kcmc'], i['jsxm'], i['xf'], i['jd'], i['njzypm'])
        grades.append(grade)
    return grades


grades = get_grade('username', 'password', '2016-2017', '1')
for item in grades:
    for (k, v) in item.items():
        print k,v