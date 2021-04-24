from parser import parse_interns
from sheets import updateTable
from flask import Flask, request
import threading
import json

app = Flask(__name__)

def run_mock(host, port):
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate = request.environ.get('werkzeug.server.shutdown')
    if terminate:
        terminate()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_mock()
    return 'Shutting down...'


@app.route('/get/interns', methods=['GET'])
def hello_world():
    return json.dumps(parse_interns())

@app.route('/update/table', methods=['POST'])
def update():
    try:
        updateTable()
        return {"status": "ok"}, 200
    except Exception as e:
        print(e)
        return {"status": "bad"}, 400

if __name__ == '__main__':
    run_mock(host='0.0.0.0', port=5000)
