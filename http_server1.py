import socket
import sys
import os

def http_server(port):

    # Configure socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', int(port)))
        sock.listen(100)
    except:
        print('[Error] Failed to bind port ' + port)
        sys.exit(1)
    else:
        print('[Message] Listening on port ' + port)

    while True:
        # maximum number of requests waiting
        try:
            conn, addr = sock.accept()
            request = bytes.decode(conn.recv(1024))
            src = request.split(' ')[1][1:]

            content = ''
            print(src)
            if os.path.exists(src):
                if not src.endswith('.htm') and not src.endswith('.html'):
                    content += "HTTP/1.0 403 Forbidden\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {}\r\n\r\n403 Forbidden".format(len("403 Forbidden"))
                else:
                    file = open(src, 'r')
                    body = file.read()
                    content += "HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {}\r\n\r\n".format(len(body))
                    content += body
                    file.close()
            else:
                content += "HTTP/1.0 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {}\r\n\r\n404 Not Found".format(len("404 Not Found"))

            conn.sendall(str.encode(content))
            conn.close()

        except Exception as e:
            print(e)
            conn.close()

if __name__ == "__main__":
    http_server(sys.argv[1])
    
