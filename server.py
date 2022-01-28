#  coding: utf-8 
import socketserver
import re
import os

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
        print ("Got a request of: %s\n" % self.data.decode("utf-8"))
        #TODO
        message = "HTTP/1.1 "
        path = self.get_path(self.data.decode("utf-8"))
        print("path is", path)
        body = ""
        content_type = "text/plain"
        #Other requests -- 405 Method Not Allowed
        if not self.check_get_method(self.data.decode("utf-8")):
            message += "405 Method Not Allowed\n"
        else:
            if path:
                # validate the path
                status_code = self.check_path(path)
                print("status code is: ",status_code)
                if status_code == 200:
                    body = self.get_body(path)
                    content_type = self.check_file(path)
                    message += "200 OK\n"
                elif status_code == 301:
                    message = message + "301 Moved Permanently\nLocation: http://127.0.0.1:8080" + path +"/\n"
                elif status_code == 404:
                    message += "404 Not Found\n"

            else:
                # no path exist
                message += "404 Not Found\n"
        

        message = message + 'Content-Type: ' + content_type + '\nContent-Length: ' + str(len(body)+1)
        #Send back response of whatever
        self.request.sendall(bytearray(message+"\r\n\r\n"+body+'\n','utf-8'))

    #Check if the request method is GET
    def check_get_method(self, data):
        if data[:3]=="GET":
            return True
        else:
            return False

    #Get the path of the request
    def get_path(self, request):
        path = re.search('/.*? HTTP', request)
        if path is not None:
            path = path.group(0).replace(" HTTP","")
            # print('path\n',path)
            return path
        else:
            return None

    #Check if the path is valid
    def check_path(self, path):
        path = "www"+path
        #for security issue
        current_path = os.getcwd()
        abs_path = os.path.abspath(path)
        if os.path.commonpath((current_path, abs_path)) != current_path:
            return 404
        # print("current_path and abs_path:",current_path, abs_path)

        if os.path.exists(path):
            if os.path.isfile(path):
                return 200
        #301 error
        if path[-1] != '/':
            path += '/'
            if os.path.exists(path):
                return 301
            else:
                print("path not exist after adding /: ",path)
                return 404
        else:
            #404 error
            if not os.path.exists(path):
                print("path not exist: ",path)
                return 404
        return 200

    #Check file mimetype
    def check_file(self, path):
        the_path = path.split('.')
        if the_path[-1] == "css":
            return "text/css"
        else:
            return "text/html"


    #Get the body of the response
    def get_body(self, path):
        try:
            with open('www'+path,'r') as file:
                text = ''.join(file.readlines())
                # print('text\n',text)
                return text
        except IsADirectoryError:
            with open('www'+path+'index.html','r') as file:
                text = ''.join(file.readlines())
                # print('text\n',text)
                return text
        except Exception as e:
            # print('error\n',e)
            return e

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
