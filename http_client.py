import traceback
import socket
import sys
import re

def request(url, redirect):
    split = url.split('://')
    if split[0] != 'http':
        print('[Error] Protocol other than http is not supported.',file=sys.stderr)
        sys.exit(1)
    if redirect > 9:
        print('[Error] Too many redirections.', file=sys.stderr)
        sys.exit(1)

    else:
        addr = split[1].split('/')
        hostAndPort = addr[0].split(':')
        host = hostAndPort[0]
        port = '80'

        if len(hostAndPort) > 1:
            port = hostAndPort[1]

        path = '/' + '/'.join(addr[1:])

        se = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        se.connect((host, int(port)))

        try:
            se.send(('GET %s HTTP/1.0\r\n' % path).encode('ascii'))
            se.send(('Host: %s:%s\r\n' % (host, port)).encode('ascii'))
            se.send(b'Cache-Control: max-age=0\r\n')
            se.send(b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n')
            se.send(b'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36\r\n')
            se.send(b'Accept-Language: en-US\r\n\r\n')
        except Exception as e:
            print("[Error] ", e, file=sys.stderr)
            
        buffer = b''
        length = 0
        while True:
            d = se.recv(128)
            buffer += d
            if buffer.find(b'\r\n\r\n') >= 0:
                break

        content = buffer.split(b'\r\n\r\n', 1)
        headerLines = content[0].split(b'\r\n')
        hasLength = False
        
        for i in range(len(headerLines)):
            if headerLines[i].find(b'Content-Type') >= 0:
                if(headerLines[i].find(b'text/html') < 0):
                    print("[Error] Receiving non HTML file", file=sys.stderr)
                    sys.exit(1)

            if headerLines[i].find(b'Content-Length') >= 0:
                hasLength = True
                length = int(re.findall(r"\d+\.?\d*",bytes.decode(headerLines[i]))[0])
                if len(content) == 1:
                    buffer = buffer + se.recv(length)
                else:
                    buffer = buffer + se.recv(length-len(content[1]))

        if not hasLength:
            while True:
                d = se.recv(1024)
                if not d:
                    break
                else:
                    buffer += d

        buffer = bytes.decode(buffer)
        se.close()

        header, html = buffer.split('\r\n\r\n', 1)
        buffer = buffer.split('\r\n')
        statusCode = int(buffer[0].split(' ')[1])
        
        if statusCode == 301 or statusCode == 302:
            for entry in buffer:
                if entry.find("Location") >= 0:
                    entry = entry.split(': ')
                    print('Redirecting to '+entry[1],file=sys.stderr)
                    request(entry[1], redirect+1)
        elif statusCode > 400:
            print(html)
            sys.exit(1)
        else:
            print(html)
            sys.exit(0)
            

if __name__ == "__main__":
    request(sys.argv[1], 0)
    
    
