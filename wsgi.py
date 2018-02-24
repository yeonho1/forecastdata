from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
from cgi import parse_qs, escape
import json
#import socket
#from wsgiref.simple_server import make_server

SERVICE_KEY = 'YOURKEYHERE'
def application(environ, start_response):
    d = parse_qs(environ['QUERY_STRING'])
    
    date = d.get('date', [''])[0]
    time = d.get('time', [''])[0]
    nx = d.get('nx', [''])[0]
    ny = d.get('ny',[''])[0]
    date = escape(date)
    time = escape(time)
    nx = escape(nx)
    ny = escape(ny)
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData' # Forecast API URI
    queryParams = '?' \
        + 'ServiceKey=' + SERVICE_KEY + '&' \
        + urlencode({
            quote_plus('base_date'): date,
            quote_plus('base_time'): time,
            quote_plus('nx'): nx,
            quote_plus('ny'): ny,
            quote_plus('numOfRows') : '184',
            quote_plus('pageNo') : '1',
            quote_plus('startPage') : '1',
            quote_plus('_type'): 'json'
        })
    print('[' + url + queryParams + ']')
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response = urlopen(request).read()
    jsonloads = json.loads(response)
    
    rain_time = []
    humidity_time = []
    lowest_time = []
    highest_time = []
    try:
        items = jsonloads['response']['body']['items']['item']
    except KeyError:
        out = {'msg':'error'}
        response_body = json.dumps(out)
        response_header = [('Content-Type','text/json'),('Content-Length',str(len(response_body)))]
        start_response('200 OK', response_header)
        return [response_body]
    out = {'rain':[],'humidity':[],'lowest':[],'highest':[]}
    for item in items:
        if item['category']=='POP': 
            rain_time = getTime(item)
            out['rain'].append({'date':rain_time[0],'time':rain_time[1],'value':item['fcstValue']})
        elif item['category']=='REH':
            humidity_time = getTime(item)
            out['humidity'].append({'date':humidity_time[0],'time':humidity_time[1],'value':item['fcstValue']})
        elif item['category']=='TMN':
            lowest_time = getTime(item)
            out['lowest'].append({'date':lowest_time[0],'time':lowest_time[1],'value':item['fcstValue']})
        elif item['category']=='TMX':
            highest_time = getTime(item)
            out['rain'].append({'date':highest_time[0],'time':highest_time[1],'value':item['fcstValue']})
    response_body = json.dumps(out)
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    
    start_response(status, response_headers)
    return [response_body]

def getTime(item):
    return [item['fcstDate'], item['fcstTime']]

#httpd = make_server(socket.gethostbyname(socket.gethostname()),8051,application)
#httpd.serve_forever()
