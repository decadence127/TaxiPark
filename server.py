from flask import Flask, request, Response
import socket
import random
import json
import sys
import os

app = Flask(__name__)
key = ''.join(random.sample(
    "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", 
    random.randint(8, 24)
))
port = 0
secret_file = os.path.join(os.environ['HOME'], '.myapp.secret')

@app.route('/<authkey>')
def hello(authkey):
    if authkey == key:
        return 'Hello, world!'
    else:
        return Response('Access Denied', 401)

def broadcast(port):
    s = json.dumps({
        'key' : key,
        'port' : port,
    'pid' : os.getpid()
    })
    f = open(
        secret_file,
        'w'
    )
    f.write(s)
    os.chmod(secret_file, 400)
    f.close()


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    broadcast(port)
    sock.close()
    app.run(port=port)