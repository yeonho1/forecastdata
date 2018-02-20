from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
from cgi import parse_qs, escape
import json

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
            quote_plus('numOfRows') : '10',
            quote_plus('pageNo') : '1',
            quote_plus('startPage') : '1',
            quote_plus('_type'): 'json'
        })
    print('[' + url + queryParams + ']')
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response = urlopen(request).read()
    jsonloads = json.loads(response)
    
    rain = None
    humidity = None
    lowest = None
    highest = None
    try:
        items = jsonloads['response']['body']['items']['item']
    except KeyError:
        out = "{'msg':'Incorrect Request'}"
        response_body = json.dumps(out)
        response_header = [('Content-Type','text/json'),('Content-Length',str(len(response_body)))]
        start_response('200 OK', response_header)
        return [response_body]
    for item in items:
        if item['category']=='POP':
            rain = item['fcstValue']
        elif item['category']=='REH':
            humidity = item['fcstValue']
        elif item['category']=='TMN':
            lowest = item['fcstValue']
        elif item['category']=='TMX':
            highest = item['fcstValue']
    out = {'rain':rain,'humidity':humidity,'lowest':lowest,'highest':highest}
    response_body = json.dumps(out)
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    
    start_response(status, response_headers)
    return [response_body]
