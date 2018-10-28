from gevent import monkey; monkey.patch_all()
from time import sleep
from bottle import route, run, get, post, request, redirect
import requests
chat = 'null'
oldchat = ''

@route('/')
def stream():
    global oldchat
    yield login()
    yield chat
    yield '<br/>'
    while True:
        if (oldchat != chat):
            yield chat
            yield '<br/>'
            oldchat = chat
        sleep(1)

@route('/add/<text>')
def add(text):
    global chat
    chat = text

@route('/redirect/<url>')
def redect(url):
    redirect(url)

@get('/input')
def login():
    return '''
        <form action="/input" method="post">
            Input: <input name="username" type="text" />
            <input value="Send" type="submit" />
        </form>
    '''

@post('/input')
def do_login():
    username = request.forms.get('username')
    data = {'content':username}
    requests.post('https://discordapp.com/api/webhooks/470585603638165505/AJI0_cSWbUSJmcwtu8MkCeGhAT-TR1ntZpY74pwCUGr9j-9cvp6lYWcKbe2PF32pvjN3', data=data)
    return '''
        <meta http-equiv="refresh" content="0; url=http://192.168.1.109:8080/stream" />
    '''
run(host='0.0.0.0', port=80, server='gevent', reloader=True)
##'<br/>'