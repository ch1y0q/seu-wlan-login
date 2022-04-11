# coding=utf-8

import requests
import re
import json
import base64
import os
import time
import platform

def PingTest():
    sysstr = platform.system()
    if(sysstr =="Windows"):
        err = os.system('ping -4 -n 1 www.baidu.com > NUL:')
    elif(sysstr == "Linux"):
        err = os.system("ping -4 -n 1 www.baidu.com > /dev/null &")
    else:
        raise OSError('Unknown OS')

    if err:
        return False
    else:
        return True

def loop():
    flag = False
    while True:
        if PingTest():
            flag = False
        else:
            if flag:
                print('正在登录……')
                login()
            else:
                print('发现网络异常')
                flag = True
                continue
        time.sleep(120)

def login():
    try:
        config_file = 'config.json'
        pattern = re.compile(r'\{.*\}')

        """
        try:
            r = requests.get('https://w.seu.edu.cn/drcom/chkstatus?callback=dr1003')
        except OSError:
            print('错误：连接失败。')
            return False

        if r.status_code != 200:
            print('错误：连接失败。')
            return False
        status = json.loads(pattern.findall(r.text)[0])

        if status['result'] == 1:
            print('错误：你已经登录了 seu-wlan。')
            return False
        elif status['result'] != 0:
            print('错误：未知错误。')
            return False
        """

        try:
            with open(config_file) as f:
                config = json.load(f)
        except IOError:
            print('错误：配置文件 config.json 不存在。')
            with open(config_file, 'w') as f:
                config = {
                    'username': '',
                    'password': '',
                    'wlan_user_ip': ''
                }
                json.dump(config, f, indent=2)
                return False

        if config['username'] == '' or config['password'] == '' or config['wlan_user_ip'] == '':
            print('错误：请在配置文件 config.json 中填写用户名、密码和userip。')
            return False

        login_url = 'http://10.80.128.2:801/eportal/?c=Portal&a=login&callback=dr1004&login_method=1&user_account=%2C0%2C' + config['username'] + '&user_password=' + config['password'] + '&wlan_user_ip=' + config['wlan_user_ip']
        try:
            r = requests.get(login_url)
        except OSError:
            print('错误：连接失败。')
            return False

        if r.status_code != 200:
            print('错误：连接失败。')
            return False
        login = json.loads(pattern.findall(r.text)[0])

        if login['result'] != '1':
            message = base64.b64decode(login['msg']).decode()
            if message == 'ldap auth error':
                print('错误：用户名或密码错误。')
            elif message == 'userid error1':
                print('错误：用户名不存在。')
            elif message == 'userid error2':
                print('错误：密码错误。')
            else:
                print('错误：登录失败。')
            return False

        print('登录成功。')
        return True

    except Exception as e:
        print(e)
        return False


loop()