import time


class Application(object):
    """web框架"""
    def __init__(self, urls):
        # 设置路由信息
        self.urls = urls

    def __call__(self, env, start_response):
        path = env.get('PATH_INFO', '/')
        print(path)
        if path.startswith('/static/'):
            file_name = path[8:]
            return static(env, start_response, file_name)
        elif path.startswith('/pic') | path.startswith('/bootstrap/') | path.endswith('.js'):
            file_name = path
            return static(env, start_response, file_name)
        else:
            for url, handler in self.urls:
                if path == url:
                    return handler(env, start_response)
            status = '404 Not Found'
            headers = []
            start_response(status, headers)
            return 'not found'


def static(env, start_response, file_name):
    status = '200 OK'
    if file_name.endswith('.jpg'):
        headers = [
            ('ContentType', 'image/*'),
            ('Server', 'My server')
        ]
        try:
            file = open('.' + file_name, 'rb')
        except IOError:
            status = '404 Not Found'
            headers = []
            start_response(status, headers)
            return 'not found'
        else:
            file_data = file.read()
            file.close()
            # 构造响应数据
            start_response(status, headers)
            return file_data
    else:
        headers = [
            ('ContentType', 'text/plain'),
            ('Server', 'My server')
        ]
        try:
            if file_name.startswith('/'):
                file_name = file_name[1:]
                print(file_name)
            file = open('./html/' + file_name, 'rb')
        except IOError:
            status = '404 Not Found'
            headers = []
            start_response(status, headers)
            return 'not found'
        else:
            file_data = file.read()
            file.close()
            # 构造响应数据
            start_response(status, headers)
            return file_data.decode('utf-8')


def index(env, start_response):
    return static(env, start_response, 'index.html')


def show_time(env, start_response):
    status = '200 OK'
    headers = [
        ('ContentType', 'text/plain')
    ]
    start_response(status, headers)
    return time.ctime()


def say_hello(env, start_response):
    status = '200 OK'
    headers = [
        ('ContentType', 'text/plain')
    ]
    start_response(status, headers)
    return 'hello my web'


urls = [
    ('/', index),
    ('/index.html',index),
    ('/ctime', show_time),
    ('/sayhello', say_hello)
]
app = Application(urls)

