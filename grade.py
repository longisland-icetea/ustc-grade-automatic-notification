#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests, os, zlib, time, getpass, sys
from mail import send_email
from config import *


def login():
    has_login = False
    while not has_login:
        print('Trying to login...')
        data={'userbz': 's','hidjym': '','userCode': student_no,'passWord': ustcmis_password}
        result = requests.post('http://mis.teach.ustc.edu.cn/login.do', params=data)
        cookies = result.cookies
        if "alert" in result.text:
            print('Login incorrect!')
        else:
            has_login = True
            print('Login OK!')
            return cookies


def parse_grade(grade):
    soup = BeautifulSoup(grade, "html5lib")
    # for i,line in enumerate(soup.find_all('tr')):
    #    for j,elem in enumerate(line.find_all('td')):
    #        print 'line=',i,' row=',j,' ',elem.get_text().encode('utf-8')
    flag = 0
    rows = soup.find_all('tr')
    data = []
    for row in rows:
        elems = row.find_all('td')
        if len(elems) == 7:
            if flag:
                data.append([td.get_text() for td in elems])
            flag = 1
    return data


olddata = []
first_run = True
cookies = dict()
while True:
    print('Query...')
    try:
        grade = requests.get('http://mis.teach.ustc.edu.cn/initfqcjxx.do?tjfs=1',cookies=cookies).text
        if "userinit" in grade:
            print('Not login.')
            cookies=login()
            continue
        data = parse_grade(grade)
        print(time.strftime('%Y-%m-%d %X', time.localtime(time.time())), 'Count :', len(data))
        test_mail = False
        if first_run:
            ans = input('Send test email? (y/n)')
            if ans.lower() in ['', 'y', 'yes']:
                test_mail = True
        if len(data) != len(olddata) and not first_run or test_mail:
            text = ' , '.join(row[2] + ' ' + row[3] for row in data if row not in olddata)
            if test_mail:
                text = 'Test email. ' + text
            print('Sending mail...')
            print('Text:', text)
            if enable_mail:
                send_email(text)
            print('Mail sent.')
        olddata = data
        first_run = False
    except Exception as e:
        if not isinstance(e, KeyboardInterrupt):
            print(time.strftime('%Y-%m-%d %X', time.localtime(time.time())), 'Error:', str(e))
        else:
            break
    time.sleep(interval)
