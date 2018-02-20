from datetime import datetime
import json
# import socket
# from wsgiref.simple_server import make_server
import time

def application(environ, start_response):
    currentTime = datetime.now().strftime('%H:%M')
    currentTime_front = int(currentTime[0:2])
    L = []
    if currentTime_front > 02:
        
        ymd = time.strftime('%Y/%m/%d')
        L.append((ymd.replace('/',''), '0200'))
        if currentTime_front > 05:
            
            ymd = time.strftime('%Y/%m/%d')
            L.append((ymd.replace('/',''), '0500'))
            if currentTime_front > 8:
                
                ymd = time.strftime('%Y/%m/%d')
                L.append((ymd.replace('/',''), '0800'))
                if currentTime_front > 11:
                    
                    ymd = time.strftime('%Y/%m/%d')
                    L.append((ymd.replace('/',''), '1100'))
                    if currentTime_front > 14:
                        
                        ymd = time.strftime('%Y/%m/%d')
                        L.append((ymd.replace('/',''), '1400'))
                        if currentTime_front > 17:
                            
                            ymd = time.strftime('%Y/%m/%d')
                            L.append((ymd.replace('/',''), '1700'))
                            if currentTime_front > 20:
                                
                                ymd = time.strftime('%Y/%m/%d')
                                L.append((ymd.replace('/',''), '2000'))
                                if currentTime_front > 23:
                                    
                                    ymd = time.strftime('%Y/%m/%d')
                                    L.append((ymd.replace('/',''), '2300'))
    response_body = json.dumps(L)
    response_header = [('Content-Type','text/json'),('Content-Length', str(len(response_body)))]
    start_response('200 OK', response_header)
    
    return [response_body]
#httpd = make_server(socket.gethostbyname(socket.gethostname()),8051,application)
# httpd.serve_forever()
    
    
    
    
    
    
                                