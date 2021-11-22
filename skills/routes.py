from flask import render_template, redirect, url_for, request
from skills import flaskapp, rpi, socket_, SOCKET_INFO
from flask_socketio import SocketIO, emit, namespace, send, disconnect
import json
import data
from data import DATA

@socket_.on('socket_connect')
def socket_connect():
    emit('connected')
    return

@socket_.on('disconnect')
def disconnecting():
    return

@socket_.on('getData')
def getTime():
    emit('data', json.dumps(DATA))
    return


# Client vragt voor data (interval) en server stuurd data als er iets is veranderd
@socket_.on('get_sensor_data')
def get_sensor_data():
    # get TMP data
    global TMP
    # # controleer op wijzigingen
    # if TMP != INPUT:
    #     TMP = INPUT.copy()
    #     emit('status', json.dumps(INPUT), broadcast=True)
    return


@flaskapp.route("/")
def home():
    return render_template('index.html', test='hoi', title='Home page')

# test
@flaskapp.route("/test")
def test():
    return render_template('test.html', test='hoi')

@flaskapp.route("/on")
def ledON():
    rpi.write('test', 1)
    # INPUT['test'] = True
    return redirect(url_for('home'))

@flaskapp.route("/off")
def ledOFF():
    # INPUT['test'] = False
    rpi.write('test', 0)
    return redirect(url_for('home'))
