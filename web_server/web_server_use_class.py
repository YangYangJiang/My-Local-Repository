import socket
from multiprocessing import Process
import re
# 设置静态文件根目录
HTML_ROOT_DIR = './html'

class HTTPServer(object):
    """HTTP服务器类"""
    def __init__(self):
        self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置地址复用
        self.s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
        # 提取用户请求的文件名
        file_name = re.match(r"\w+ +(/[^ ]*) ", request_startline).group(1)
        # 设置默认路径
        if '/' == file_name:
            file_name = '/index.html'
        # 打开文件读取内容
        try:
            file = open(HTML_ROOT_DIR + file_name, 'rb')
        except IOError:
            response_startline = 'HTTP/1.1 404 Not Found\r\n'
            response_body = "The file is not found"
        else:
            file_data = file.read()
            file.close()
            # 构造响应数据
            response_startline = 'HTTP/1.1 200 OK\r\n'
            response_body = file_data.decode('utf-8')
        finally:
            response_headers = 'Server:My server\r\n'
            response_data = response_startline + response_headers + '\r\n' + response_body
        print("ResponseData: ", response_data)
        # 向客户端返回响应数据，如果在python3中，发送数据要用bytes()转换
        cliSocket.send(bytes(response_data, 'utf-8'))
        # 关闭客户端连接
        cliSocket.close()

def main():
    http_server = HTTPServer()
    http_server.bind(8000)
    http_server.start()

if __name__ == "__main__":
    main()
