#  coding: utf-8 
import socketserver
from os import path

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
        splt = self.data.decode('utf-8').split(' ')
        response = None
        if splt[0] == 'GET':
            self.GET(splt[1])
        else:
            response = 'HTTP/1.1 405 Method Not Allowed\r\n'
            response += 'Content-Type: text/plain\r\n'
            response += 'Connection: close\r\n\r\n'
            self.request.sendall(bytearray(response, 'utf-8'))
    
    def handle_redirect(self, location):
        location = location + '/'
        response = 'HTTP/1.1 301 Moved Permanently\r\n'
        response += 'Connection: close\r\n\r\n'

        return response, location
    
    def handle_ok(self, user_path):
        if path.isfile(user_path + 'index.html'):
            content_type = 'text/html' if user_path.endswith('.html') else 'text/css'
            with open(user_path + 'index.html', 'r') as file:
                content = file.read()
            response = 'HTTP/1.1 200 OK Not FOUND!' + '\r\n'
            response += 'Location: ' + user_path + '\r\n'
            response += 'Content-type: ' + content_type + '\r\n'
            response += 'Connection: close' + '\r\n\r\n'
        elif user_path.endswith('index.html'):
            content_type = 'text/html' if user_path.endswith('.html') else 'text/css'
            if path.isdir(user_path):
                with open(user_path, 'r') as file:
                    content = file.read()
            else:
                response = 'HTTP/1.1 200 OK Not FOUND!' + '\r\n'
                response += 'Location: ' + user_path + '\r\n'
                response += 'Content-type: ' + content_type + '\r\n'
                response += 'Connection: close' + '\r\n\r\n'
        else:
            content_type = 'text/html' if user_path.endswith('.html') else 'text/css'
            response = 'HTTP/1.1 200 OK Not FOUND!' + '\r\n'
            response += 'Location: ' + user_path + '\r\n'
            response += 'Content-type: ' + content_type + '\r\n'
            response += 'Connection: close' + '\r\n\r\n'

        return response

    def handle_not_found(self):
        response = 'HTTP/1.1 404 ERROR NOT FOUND\r\n\r\n'

        return response

    def GET(self, dir):
        user_path = '.' + dir
        base_dir = './www'
        response = 'OK'

        if not user_path.endswith('/') and path.isfile(user_path + '/index.html'):
            response, user_path = self.handle_redirect(user_path)
            self.request.sendall(bytearray(response, 'utf-8'))
        if path.isdir(base_dir + '/' + user_path) or user_path.endswith('/base.css') or user_path.endswith('/index.html'):
            response = self.handle_ok(user_path)
        else:
            response = self.handle_not_found()

    #     user_path = '.' + dir
    #     base_dir = './www'
    #     print(user_path, path.isdir(user_path), user_path.endswith('/'), base_dir)
    #     if not user_path.startswith(base_dir) and path.isdir(user_path):
    #         response = 'HTTP/1.1 403 FORBIDDEN\r\n\r\n'

    #     elif path.isdir(user_path) and not user_path.endswith('/'):
    #         # Perform a 301 redirect by appending a trailing slash
    #         location = str(user_path) + '/'
    #         response = 'HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nConnection: close\r\n\r\n'
    #         response += 'Location: ' + location
    #     elif path.isdir(user_path) and user_path.endswith('/'):
    #             print('first check')
    #             if path.isfile(user_path + 'index.html'):
    #                 user_path += 'index.html'
    #                 content_type = 'text/html' if user_path.endswith('.html') else 'text/css'
    #                 with open(user_path, 'r') as file:
    #                     content = file.read()
    #                 response = 'HTTP/1.1 200 OK'
    #                 response += 'Location: ' + user_path
    #                 response += 'Content-Length: ' + len(content)
    #                 response += 'Connection: close'
    #                 self.request.sendall(bytearray(response, 'utf-8'))
    #                 print('200-1') 
    #             else:
    #                 response = 'HTTP/1.1 404 ERROR NOT FOUND\r\n\r\n'
    #                 print('404-1')
    #     elif path.exists(user_path) and path.isfile(user_path):
    #         # Read the content of the file and send it as the response
    #         content_type = 'text/html' if user_path.endswith('.html') else 'text/css'
    #         with open(user_path, 'r') as file:
    #             content = file.read()
    #         response = 'HTTP/1.1 200 OK'
    #         response += 'Location: ' + user_path
    #         response += 'Content-Length: ' + len(content)
    #         response += 'Connection: close'
    #         response += 'Content: ' + content
    #         print('200-1')
    #     else:
    #         # Return a 404 response if the file is not found
    #         response = 'HTTP/1.1 404 ERROR NOT FOUND\r\n\r\n'
    #         print('404-2')

        print(response)
        self.request.sendall(bytearray(response, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
