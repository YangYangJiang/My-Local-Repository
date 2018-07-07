import time
def application(env, start_response):
    # env.get('Method')
    # env.get('PATH_INFO')
    status = '200 OK'
    headers = [
        ('Server', 'My server'),
        ('Content-Type', 'text/plain')
    ]
    start_response(status, headers)
    return time.ctime()
