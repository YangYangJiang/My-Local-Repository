import socket
from multiprocessing import Process
import re
import sys


class HTTPServer(object):
    """HTTP服务器类"""
    def __init__(self, application):
        self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置地址复用
        self.s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.app = application
        self.response_headers = None

    def bind(self, port):
        self.s_socket.bind(('', port))

    def start(self):
        self.s_socket.listen(128)
        while True:
            cliSocket, cliAddr = self.s_socket.accept()
            print("[%s,%s]用户连接上了" % cliAddr)
            p = Process(target=self.handle_client, args=(cliSocket,))
            p.start()
            cliSocket.close()

    def start_response(self, status, headers):
        response_headers = 'HTTP/1.1 '+status+'\r\n'
        for head in headers:
            response_headers += '%s: %s\r\n' % head
        self.response_headers = response_headers

    def handle_client(self, cliSocket):
        """处理客户端请求"""
        # 获取客户端请求数据
        request_data = cliSocket.recv(1024)
        print("RequestData: ")
        # 解析请求报文
        request_line = request_data.splitlines()
        for line in request_line:
            print(line)
        request_startline = request_line[0].decode('utf-8')
        # 提取用户请求的路径
        userpath = re.match(r"\w+ +(/[^ ]*) ", request_startline).group(1)
        # 设置默认路径
        env = {
            'PATH_INFO': userpath,
        }
        response_body = self.app(env, self.start_response)
        # response_data = self.response_headers + '\r\n' + response_body
        # 向客户端返回响应数据，如果在python3中，发送数据要用bytes()转换
        cliSocket.send(bytes(self.response_headers + '\r\n', 'utf-8'))
        if isinstance(response_body, str):
            cliSocket.send(bytes(response_body, 'utf-8'))
        else:
            cliSocket.send(response_body)
        # 关闭客户端连接
        cliSocket.close()


def main():
    if len(sys.argv)<2:
        sys.exit('python MyWebServer.py Moudle:app')
    moudle_name, app_name = sys.argv[1].split(':')
    m = __import__(moudle_name)
    app = getattr(m, app_name)
    http_server = HTTPServer(app)
    http_server.bind(8000)
    http_server.start()


if __name__=='__main__':
    main()
