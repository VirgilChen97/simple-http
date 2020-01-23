import socket
import sys
import os
import json

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

            print('[Message] Connect by: ' + str(addr))
            print('[Message] Request is:\n' + str(request))
            print('[Message] is:\n' + str(src))
            content = ''
            #product?a=12&b = 60 & another = 0.5&
            if src.startswith('/product'):
                src = src + '&'
                start_e = 0
                start_a = 0
                ans = 1
                no_error = True
                while src.find('=', start_e) >= 0:  # As long as '=' exists in src
                    start_e = src.find('=', start_e) + 1
                    start_a = src.find('&', start_a) + 1
                    try:
                        ans = ans * float(src[start_e:start_a - 1])
                        form = {
                            "operation": "product",
                            "operands":float(src[start_e:start_a - 1]),
                            "result": ans
                        }
                        res = json.dumps(form, indent=4, separators=",")
                    except ValueError:
                        # ValueError during convert, valid input
                        no_error = False
                        break
                if no_error:
                    content += res
                    content += "HTTP/1.0 200 OK\r\nContent-Type:application/json;charset=UTF-8\r\n\r\n"
                else:
                    content += ('Invalid input')
                    content += "HTTP/1.0 400 Fail\r\nContent-Type: son; charset=UTF-8\r\n\r\n"
                    #content += file.read()
                    #file.close()
            else:
                content += "HTTP/1.0 404 Not Found\r\n\r\n404 Not Found"

            conn.sendall(str.encode(content))
            conn.close()

        except Exception as e:
            print(e)


if __name__ == "__main__":
    http_server(sys.argv[1])

