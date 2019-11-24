import socket
import os,time
from threading import Thread


class RequestThread(Thread):

    def __init__(self, threadNo, thread_connection):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.connection = thread_connection


    def run(self):
        intialRequest = self.connection.recv(1024)
        print intialRequest

        request,method = GetRequestDict(intialRequest)
        
        http_response = handleRequest(request)

        #print http_response
        self.connection.sendall(http_response)
        self.connection.close()
        time.sleep(5)
        print "Thread is closing", self.threadNo


def GetRequestDict(request):
    ret = dict()
    requestlist = request.split('\n')
    for requestelement in requestlist:
        Headers = requestelement.split(' ')
        
        if len(Headers) >= 2:
            ret[Headers[0]] = Headers[1]
            if Headers[0]=="GET":
                method = "GET"
                ret["Version"] = Headers[2]
                ret["GET"] = ret["GET"][1:]
                return ret,method



def handleRequest(request):
    if request["GET"] not in os.listdir("./"):
        http_response = """\
HTTP/1.1 200 OK

<html>
<h1>404 Not Found!</h1>
</html>
"""
    else:
        with open(request["GET"]) as f:
            http_response = """\
HTTP/1.1 200 OK

"""
            for line in f:
                http_response += line

    return http_response



def Main():

	HOST, PORT = '10.0.2.15', 9991

	socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	socket_listen.bind((HOST, PORT))
	socket_listen.listen(5)
	print 'Serving HTTP on port %s ...' % PORT

	requestList = list()

	while True:
		client_connection, client_address = socket_listen.accept()

		newRequest = RequestThread(len(requestList), client_connection)
		print '\nStarting Thread %s ....\n' % len(requestList)
		newRequest.start()
		requestList.append(newRequest)

		for request in requestList:
			if not request.isAlive():
				requestList.remove(request)
				request.join()



# if __name__() == __main__():
Main()