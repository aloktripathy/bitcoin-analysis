from bottle import route, run, template


HOST = 'localhost'
PORT = 8080


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host=HOST, port=PORT, reloader=True)
