import socket
import os
import re
import atexit
def http_server(port):

    # Configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 8082))
    sock.listen(100)

    # infinite loop
    while True:
        # maximum number of requests waiting
        try:
            conn, addr = sock.accept()
            request = bytes.decode(conn.recv(1024))
            src = request.split(' ')[1]

            print ('Connect by: ', addr)
            print ('Request is:\n', request)
            
            content = ''
            if os.path.exists(src[1:]):
                file = open(src[1:], 'r')
                content += "HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                content += file.read()
                file.close()
            else:
                content += "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n404 Not Found"

            conn.sendall(str.encode(content))
            conn.close()

        except Exception as e:
            print(e)

if __name__ == "__main__":
    http_server(80)
    
