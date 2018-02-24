from urllib2 import Request, urlopen
from datetime import datetime
import time
from urllib import urlencode, quote_plus
import json
#from wsgiref.simple_server import make_server
#import socket

SERVICE_KEY = 'YOURKEYHERE'
def application(environ, start_response):
    date = datetime.strftime('%Y%m%d')
    times = ['02','05','08','11','14','17','20','23']
    if time.strftime('%H') in times:
        time = '%s00' % time.strftime('%H')
    else:
        if str(int(time.strftime('%H')) - 1) in times:
            time = '%s00' % str(int(time.strftime('%H')) - 1)
        elif str(int(time.strftime('%H')) - 2) in times:
            time = '%s00' % str(int(time.strftime('%H')) - 2)
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData' # Forecast API URI
    queryParams = '?' \
        + 'ServiceKey=' + SERVICE_KEY + '&' \
        + urlencode({
            quote_plus('base_date'): date,
            quote_plus('base_time'): time,
            quote_plus('nx'): '60',
            quote_plus('ny'): '127',
            quote_plus('numOfRows') : '184',
            quote_plus('pageNo') : '1',
            quote_plus('startPage') : '1',
            quote_plus('_type'): 'json'
        })
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response = urlopen(request).read()
    jsonloads = json.loads(response)
    avtimes = []
    try:
        items = jsonloads['response']['body']['items']['item']
    except KeyError:
        out = {'msg':'error'}
        response_body = json.dumps(out)
        response_header = [('Content-Type','text/json'),('Content-Length',str(len(response_body)))]
        start_response('200 OK', response_header)
        return [response_body]
    for x in items:
        if (x['fcstDate'],x['fcstTime']) in avtimes:
            pass
        elif (x['fcstDate'],x['fcstTime']) not in avtimes:
            avtimes.append((x['fcstDate'],x['fcstTime']))
    response_body = json.dumps(avtimes)
    response_header = [('Content-Type','text/json'),('Content-Length',str(len(response_body)))]
    start_response('200 OK', response_header)
    return [response_body]
#httpd = make_server(socket.gethostbyname(socket.gethostname()),8051,application)
#httpd.serve_forever
    