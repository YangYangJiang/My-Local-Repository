import os
PICPATH = '/pic'


def application(env, start_response):
    # print(os.getcwd())
    foldername = os.getcwd()+PICPATH+'/'+env.get('key')
    picturenum = int(env.get('num'))
    piclist = os.listdir(foldername)
    picname = foldername+'/'+piclist[picturenum]
    print(picname)
    f = open(picname, 'rb')
    data = f.read()
    f.close()
    status = '200 OK'
    headers = [
        ('Server', 'My server'),
        # ('Content-Type', 'image/*'),
    ]
    start_response(status, headers)
    return data
