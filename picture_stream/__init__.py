from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import inotify.adapters
import threading
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    print('myEvent received')
    emit('my_response', {'data': message['data']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_message(message):
    emit('my_response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    print('connected')
    emit('my_response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


def fs_watch():
    known_files = []
    i = inotify.adapters.Inotify()
    i.add_watch('/tmp/photos')
    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if filename in known_files:
            continue
        if type_names in [['IN_CLOSE_WRITE'], ['IN_MOVED_TO']] and filename.lower().endswith('jpg'):
            print(filename)
            os.system(f'convert {path}/{filename} -crop 1620x2880+1550+280 +repage '
                      f'-resize 1080x1920 -quality 85 img/{filename}')
            socketio.emit('my_response', {'data': {'filename': f'img/{filename}'}}, namespace='/test')
            known_files.append(filename)


if __name__ == '__main__':
    threading.Thread(target=fs_watch).start()
    socketio.run(app, host='0.0.0.0')
