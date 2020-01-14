import socket
import sys

def request(url, redirect):
    splited = url.split('://')
    if splited[0] == 'https':
        print('[Error] https protocol is not supported.')
        return 1;
    if redirect > 9:
        print('[Error] Too many redirections.')
        return 1;

    else:
        addr = splited[1].split('/')
        host = addr[0]
        path = '/' + '/'.join(addr[1:])

        se = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        se.connect((host, 80))

        try:
            se.send(str.encode('GET %s HTTP/1.1\r\n' % path))
            se.send(str.encode('Host: %s:80\r\n' % host))
            se.send(b'Connection: keep-alive\r\n')
            se.send(b'Cache-Control: max-age=0\r\n')
            se.send(b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n')
            se.send(b'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36\r\n')
            se.send(b'Accept-Encoding: gzip, deflate, sdch\r\n')
            se.send(b'Accept-Language: zh-CN,zh;q=0.8\r\n\r\n')
        except Exception as e:
            print(e)

        buffer = []
        while True:
            d = se.recv(1024)
            if d:
                buffer.append(d)
            else:
                break

        for i in range(len(buffer)):
            buffer[i] = bytes.decode(buffer[i]);

        buffer = ''.join(buffer)
        se.close()

        header, html = buffer.split('\r\n\r\n', 1)
        buffer = buffer.split('\r\n')
        
        if buffer[0].find('302') == -1 and buffer[0].find('301') == -1:
            print(html)
            return 0
        else:
            for entry in buffer:
                if entry.find("Location") >= 0:
                    entry = entry.split(': ')
                    request(entry[1], redirect+1)

if __name__ == "__main__":
    request('http://insecure.stevetarzia.com', 0)
    
    
