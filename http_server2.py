import socket
import select
import sys
import os
import queue
 
 
def http_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", int(port)))
    sock.listen(128)
    sock.setblocking(False)

    inputs = [sock]
    outputs = []
    message_queues = {}

    while inputs:

        print('[Message] Waiting for new client')
        re, we, ex = select.select(inputs, outputs, inputs)
        print(re, we)

        for s in re:
            if s is sock:
                new_socket, new_addr = sock.accept()
                print('[Message] New connection from' + str(new_addr))
                new_socket.setblocking(False)   
                inputs.append(new_socket)
                message_queues[new_socket] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    print('[Message] ' + str(s.getpeername())+' Connection closing')
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in we:
            try:
                request = message_queues[s].get_nowait()
                request = bytes.decode(request)
            except queue.Empty:
                # No messages waiting so stop checking
                # for writability.
                print('[Error] ' + str(s.getpeername())+' has no data in request or invalid encoding')
                outputs.remove(s)
            else:
                print('[Message] Sending response to '+ str(s.getpeername()))
                s.send(process(request).encode('ascii'))
                outputs.remove(s)
                inputs.remove(s)
                print('[Message] ' + str(s.getpeername())+' Connection closing')
                s.close()
        
        for s in ex:
            print('[Error] exception condition on', str(s.getpeername()))
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
 
 
def process(request):
    if not request:
        return
    content = ''
    try:
        src = request.split(' ')[1][1:]

        if os.path.exists(src):
            if not src.endswith('.htm') and not src.endswith('.html'):
                content += "HTTP/1.0 403 Forbidden\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
            else:
                file = open(src, 'r')
                body = file.read();
                content += "HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {}\r\n\r\n".format(len(body))
                content += body
                file.close()
        else:
            content += "HTTP/1.0 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n404 Not Found"
    except:
        content += "HTTP/1.0 400 Bad Request\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n400 Bad Request"

    return content

if __name__ == "__main__":
    http_server(sys.argv[1])
