import os
import socketserver

# Jiachen Xu
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
            
    def handle(self):
    
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        # print(str(self.data).split('\\r\\n'))
        detail = str(self.data.decode('utf-8')).split('\r\n')[0].split(' ')
        # print(detail)
        action = detail[0]
        url = detail[1]
        path = os.getcwd()
        
        if '../' in url:
            self.request.sendall(bytearray("HTTP/1.0 404 NOT FOUND\r\nFile Not Found",'utf-8'))
            return

        if action == 'GET':
            if url[-1]=='/':
                try:
                    file = open("./www"+url+'index.html')
                    # print(f'{path}/www/index.html')
                    content = file.read()
                    file.close()
                    self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n{content}','utf-8'))
                    
                except FileNotFoundError:
                    self.request.sendall(bytearray("HTTP/1.0 404 NOT FOUND\r\nFile Not Found",'utf-8'))
                
            elif url[-1]!='/':
                if url[-5:] == '.html':
                    try:
                        file = open("./www"+url)
                        content = file.read()
                        file.close()
                        self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n{content}','utf-8'))
                        
                    except FileNotFoundError:
                        self.request.sendall(bytearray("HTTP/1.0 404 NOT FOUND\r\nFile Not Found",'utf-8'))
                        
                elif url[-4:] == '.css':
                    try:
                        file = open("./www"+url)
                        content = file.read()
                        file.close()
                        self.request.sendall(bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: {len(content)}\r\n\r\n{content}','utf-8'))
                        
                    except FileNotFoundError:
                        self.request.sendall(bytearray("HTTP/1.0 404 NOT FOUND\r\nFile Not Found",'utf-8'))
                        
                elif os.path.exists(path+'/www'+url):
                    self.request.sendall(bytearray(f"HTTP/1.0 301 moved permanently to http://127.0.0.1:8080{url}/",'utf-8'))
                
                else:
                    self.request.sendall(bytearray("HTTP/1.0 404 NOT FOUND\r\nFile Not Found",'utf-8'))

            else:
                self.request.sendall(bytearray("HTTP/1.0 404 NOT FOUND\r\nFile Not Found",'utf-8'))
                    
        else:
            self.request.sendall(bytearray("HTTP/1.0 405 Method Not Allowed",'utf-8'))
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
