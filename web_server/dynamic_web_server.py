import socket
from multiprocessing import Process
import re
import sys
# 设置静态文件根目录
HTML_ROOT_DIR = './html'
PATH = './wsgipython'

class HTTPServer(object):
    """HTTP服务器类"""
    def __init__(self):
        self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置地址复用
        self.s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            p.join()

    def start_response(self, status, headers):
        response_header = 'HTTP/1.1 '+status+'\r\n'
        for head in headers:
            response_header += '%s: %s\r\n' % head
        self.response_headers = response_header

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
        # 提取用户请求的文件名，请求方式
        file_name = re.match(r"\w+ +(/[^ ]*) ", request_startline).group(1)
        method = re.match(r"(\w+) +/[^ ]* ", request_startline).group(1)
        querys = file_name.split('?')[1:]
        if file_name.endswith(".py"):
            # 执行py文件
            m = __import__(file_name[1:-3])
            env = {
                'PATH_INFO': file_name,
                'METHOD': method
            }
            response_body = m.application(env, self.start_response)
            # response_data = self.response_headers+response_body
        elif len(file_name.split('?'))>1:
            for query in querys:
                key = query.split('=')[0]
                value = query.split('=')[1]
                m = __import__(file_name.split('?')[0][1:])
                env = {
                    'key': key,
                    'num': value,
                    'PATH_INFO': file_name,
                    'METHOD': method
                }
                response_body = m.application(env, self.start_response)
                # response_data = self.response_headers + response_body
                # print(response_data)
        # 设置默认路径
        elif '/' == file_name:
            file_name = '/index.html'
            # 打开文件读取内容
            try:
                file = open(HTML_ROOT_DIR + file_name, 'rb')
            except IOError:
                status = '404 Not Found'
                response_body ="The file is not found"
            else:
                file_data = file.read()
                file.close()
                # 构造响应数据
                status = '200 OK'
                response_body = file_data.decode('utf-8')
            finally:
                headers = [
                    ('Server', 'My server'),
                    ('Content-Type', 'text/plain')
                ]
                self.start_response(status, headers)
                # response_data = response_headers + response_body
            # print("ResponseData: ", response_headers)
        # 向客户端返回响应数据，如果在python3中，发送数据要用bytes()转换
        cliSocket.send(bytes(self.response_headers, 'utf-8'))
        cliSocket.send(response_body)
        # 关闭客户端连接
        cliSocket.close()


def main():
    sys.path.insert(1, PATH)
    http_server = HTTPServer()
    http_server.bind(8000)
    http_server.start()


if __name__ == "__main__":
    main()
