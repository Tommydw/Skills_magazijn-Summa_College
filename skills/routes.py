from flask import render_template, redirect, url_for, request
from skills import flaskapp, rpi, socket_, SOCKET_INFO
from skills.loop import INPUT
from flask_socketio import SocketIO, emit, namespace, send, disconnect
import json

# kopieer de INPUT tabel naar TMP voor wijzigingen te detecteren
TMP = INPUT.copy()

@socket_.on('socket_connect')
def socket_connect():
    SOCKET_INFO['active'] += 1
    get_users()
    return

@socket_.on('disconnect')
def disconnecting():
    SOCKET_INFO['active'] -= 1
    get_users()
    return

# send user count
@socket_.on('get_users')
def get_users():
    emit('send_users', str(SOCKET_INFO['active']), broadcast=True)
    return

# Stuur INPUT data naar client
@socket_.on('get_status')
def get_status(): 
    emit('status', json.dumps(INPUT), broadcast=True)
    return

# Client vragt voor data (interval) en server stuurd data als er iets is veranderd
@socket_.on('get_sensor_data')
def get_sensor_data():
    # get TMP data
    global TMP
    # controleer op wijzigingen
    if TMP != INPUT:
        TMP = INPUT.copy()
        emit('status', json.dumps(INPUT), broadcast=True)
    return


@flaskapp.route("/")
def home():
    return render_template('test.html', test='hoi')


# test
@flaskapp.route("/on")
def ledON():
    rpi.write('test', 1)
    INPUT['test'] = True
    return redirect(url_for('home'))

@flaskapp.route("/off")
def ledOFF():
    INPUT['test'] = False
    rpi.write('test', 0)
    return redirect(url_for('home'))
