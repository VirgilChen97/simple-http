import socket
import sys
import re

def request(url, redirect):
    splited = url.split('://')
    if splited[0] != 'http':
        print('[Error] Protocol other than http is not supported.')
        sys.exit(1)
    if redirect > 9:
        print('[Error] Too many redirections.')
        sys.exit(1)

    else:
        addr = splited[1].split('/')
        hostAndPort = addr[0].split(':')
        host = hostAndPort[0]
        port = '80'

        if len(hostAndPort) > 1:
            port = hostAndPort[1];

        path = '/' + '/'.join(addr[1:])

        se = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        se.connect((host, int(port)))

        try:
            se.send(str.encode('GET %s HTTP/1.0\r\n' % path))
            se.send(str.encode('Host: %s:%s\r\n' % (host, port)))
            se.send(b'Cache-Control: max-age=0\r\n')
            se.send(b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n')
            se.send(b'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36\r\n')
            se.send(b'Accept-Language: en-US\r\n\r\n')
        except Exception as e:
            print(e)

        buffer = b''
        length = 0
        while True:
            d = se.recv(128)
            buffer += d;
            if buffer.find(b'\r\n\r\n') >= 0:
                break

        content = buffer.split(b'\r\n\r\n', 1)
        headerLines = content[0].split(b'\r\n')
        hasLength = False
        for i in range(len(headerLines)):
            if headerLines[i].find(b'Content-Length') >= 0:
                hasLength = True
                length = int(re.findall(r"\d+\.?\d*",bytes.decode(headerLines[i]))[0])
                if len(content) == 1:
                    buffer = buffer + se.recv(length)
                else:
                    buffer = buffer + se.recv(length-len(content[1]))
                break

        if not hasLength:
            while True:
                d = se.recv(128)
                if not d:
                    break
                else:
                    buffer += d;

        buffer = bytes.decode(buffer)
        se.close()

        header, html = buffer.split('\r\n\r\n', 1)
        buffer = buffer.split('\r\n')
        
        if buffer[0].find('302') == -1 and buffer[0].find('301') == -1:
            print(html)
            sys.exit(0)
        else:
            for entry in buffer:
                if entry.find("Location") >= 0:
                    entry = entry.split(': ')
                    request(entry[1], redirect+1)

if __name__ == "__main__":
    request(sys.argv[1], 0)
    
    
