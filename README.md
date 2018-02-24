# GITHUB FORECASTDATA by yeonho1
공공데이터 동네 예보 조회 서비스를 사용해서 값을 얻어오고 다시 내보내는 코드

## wsgi.py
**wsgi.py**는 공공데이터 동네예보조회서비스에 **요청**을 보내 **응답**을 받아 간단히 줄여 다시 사용자에게 응답을 합니다.

**유의사항**:앞부분의 ```SERVICE_KEY = 'YOURKEYHERE'```를 **그대로 사용하지 마시고** 가지고 계신 키를 ```'SERVICE_KEY'```와 같이 넣어주세요. (안 그러면 응답이 제대로 오지 않습니다.)

## wsgi2.py
**wsgi2.py**는 현재 시간을 이용해 사용자가 [**wsgi.py**] (##wsgi.py) 파일에 요청에 얻을 수 있는 기상정보의 발표시간을 알아내 응답을 하는 코드입니다.

**유의사항**: 파이썬 3로 실행시 모듈 에러가 발생할 수 있으니 파이썬 2로 실행해 주시고 아파치(Apache) 서버에 연동할 경우에는 **/etc/httpd/conf.d/** 디렉토리 안에 **원하는 이름.conf** 파일을 만들고 다음과 같이 입력해 주시면 됩니다.
###아파치 연동할 때의 .conf
```
WSGIScriptAlias /<wsgi.py에 원하는주소> /github clone한 디렉토리/wsgi.py
WSGIScriptAlias /<wsgi2.py에 원하는주소> /github clone한 디렉토리/wsgi2.py  
```
**다음은 .conf 파일의 예시입니다.**
![예시](https://preview.ibb.co/nA413H/Ex1.png)

##테스트 할 때
테스트할 때에는 (아파치 사용시 a가 wsgi.py에 원하는주소이고 b가 wsgi2.py에 원하는주소라고 가정합니다.)  
 - 아파치(또는 다른 daemon)에 연동시켰을 경우 : 서버IP/a또는b
 - 그냥 .py로 돌렸을 경우 : 서버IP:8051  
 **유의사항**: 그냥 .py를 ```python wsgi.py```로 돌렸을 때에는 한번에 한가지 요청 밖에 받을 수 없기 때문에 실제로 사용할 때에는 [***아파치에 연동***] (###아파치 연동할 때의 .conf)을 사용하는 것을 추천합니다. 그리고 .py를 사용할 때에는 앞부분과 뒷부분을 조금 수정해 주어야 하는데, 다음과 같이 수정해 주시면 됩니다.
###wsgi.py의 앞부분
```python
from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
from cgi import parse_qs, escape
import json
import socket
from wsgiref.simple_server import make_server
``` 
###wsgi.py의 뒷부분
```python
httpd = make_server(socket.gethostbyname(socket.gethostname()),
8051,application)

httpd.serve_forever()
```

###wsgi2.py의 앞부분
```python
from datetime import datetime
import json
import socket
from wsgiref.simple_server import make_server
import time
```
###wsgi2.py의 뒷부분
```python
httpd = make_server(socket.gethostbyname(socket.gethostname()),8051,application)
httpd.serve_forever()
```

**유의사항(.py 사용할 경우 해당)**: **/etc/hosts**가 127.0.0.1일 경우 socket.gethostbyname())이 작동하지 않습니다. ifconfig를 사용하여 IP 를 알아내 스트링으로 적어주세요. (아래 예시)
###예시
```python
httpd = make_server('192.168.0.2',8051,application)
httpd.serve_forever()
```
                                            