import socket
import select
import sys
import os
 
 
def http_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(128)
    sock.setblocking(False)
    socket_list = list()

    while True:
        try:
            new_socket, new_addr = sock.accept()
        except Exception as e:
            print("No new client now")  # for test
        else:
            new_socket.setblocking(False)   
            socket_list.append(new_socket)

        rs,ws,es=select.select(socket_list,[],[])

        for client_socket in rs:
            try:
                request = client_socket.recv(1024).decode('utf-8')
            except Exception as ret:
                print('1')  # for test
            else:
                if request:
                    response = process(request)
                    client_socket.sendall(str.encode(response))
                    client_socket.close()
                    socket_list.remove(client_socket)  

        print(socket_list)
 
 
def process(request):
    if not request:
        return

    src = request.split(' ')[1][1:]
    content = ''

    if os.path.exists(src):
        if not src.endswith('.htm') and not src.endswith('.html'):
            content += "HTTP/1.0 403 Forbidden\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
        else:
            file = open(src, 'r')
            content += "HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
            content += file.read()
            file.close()
    else:
        content += "HTTP/1.0 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n404 Not Found"

    return content;

if __name__ == "__main__":
    http_server(8081)
