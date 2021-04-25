from parser import parse_interns
from pg_client import get_pg_client
from sheets import updateTable
from flask import Flask, request
import threading
import json
import requests
import os

app = Flask(__name__)

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
if POSTGRES_HOST is None:
    POSTGRES_HOST = 'localhost'


def run_server(host, port):
    server = threading.Thread(target=app.run, kwargs={
                              'host': host, 'port': port})
    server.start()
    return server


def shutdown_server():
    terminate = request.environ.get('werkzeug.server.shutdown')
    if terminate:
        terminate()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Shutting down...'


@app.route('/get/interns', methods=['GET'])
def get_interns():
    return json.dumps(parse_interns())


@app.route('/update/table', methods=['POST'])
def update():
    try:
        updateTable()
        return {"status": "ok"}, 200
    except Exception as e:
        print(e)
        return {"status": "bad"}, 400


@app.route('/get/wait/<chat_id>', methods=['GET'])
def get_wait(chat_id):
    cli = get_pg_client(POSTGRES_HOST)
    cur = cli.cursor()
    cur.execute(f"select * from waitlist where chat_id = '{chat_id}'")
    if len(cur.fetchall()) == 0:
        return {
            "status": False
        }, 400
    return {
        "status": True
    }


@app.route('/set/wait/<chat_id>', methods=['POST'])
def set_wait(chat_id):
    cli = get_pg_client(POSTGRES_HOST)
    cur = cli.cursor()
    cur.execute(f"select * from waitlist where chat_id = '{chat_id}'")
    if len(cur.fetchall()) != 0:
        return {
            "status": False
        }, 400
    cur.execute(f"insert into waitlist values ('{chat_id}')")
    cli.commit()
    cur.close()
    cli.close()
    return {
        "status": True
    }


@app.route('/delete/wait/<chat_id>', methods=['POST'])
def delete_wait(chat_id):
    cli = get_pg_client(POSTGRES_HOST)
    cur = cli.cursor()
    cur.execute(f"select * from waitlist where chat_id = '{chat_id}'")
    if len(cur.fetchall()) == 0:
        return {
            "status": False
        }, 400
    cur.execute(f"delete from waitlist where chat_id = '{chat_id}'")
    cli.commit()
    cur.close()
    cli.close()
    return {
        "status": True
    }


@app.route('/notify', methods=['POST'])
def notify():
    cli = get_pg_client(POSTGRES_HOST)
    cur = cli.cursor()
    cur.execute(f"select * from waitlist")
    for chat_id in cur.fetchall():
        requests.post("https://api.telegram.org/bot1689523202:AAHxU42-E8DEBpHpnWwGunxnccwER15EB2Y/sendMessage",
                      data={
                          'chat_id': chat_id[0],
                          'text': 'Доступны новые стажировки!'
                      })

    return {
        "success": True
    }, 200


if __name__ == '__main__':
    run_server(host='0.0.0.0', port=5000)
