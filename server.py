#  coding: utf-8 
import socketserver

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
        body = self.get_body(path)
        if self.check_get_method(self.data.decode("utf-8")):
            #Handle the GET request
            message += "200 OK\n"
        else:
            #Other requests -- 405 Method Not Allowed
            message += "405 Method Not Allowed\n"

        message = message + 'Content-Length: ' + str(len(body))
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
        return "/"
        #TODO handle 301 error
        #TODO handle 404 error

    #Get the body of the response
    def get_body(self, path):
        try:
            with open('www/index.html','r') as file:
                text = ''.join(file.readlines())
                print('text\n',text)
                return text
        except Exception as e:
            print('error\n',e)
            return e

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
