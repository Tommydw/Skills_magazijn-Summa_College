from flask import render_template, redirect, url_for, request
from skills import flaskapp, rpi, socket_, SOCKET_INFO
from flask_socketio import SocketIO, emit, namespace, send, disconnect
import json
import copy
from data import DATA

@socket_.on('socket_connect')
def socket_connect():
    emit('connected')
    return

@socket_.on('disconnect')
def disconnecting():
    return

@socket_.on('getData')
def getTime(oldData, getType):
    TMP = copy.deepcopy(DATA)
    if getType == 'full': 
        TMP['type'] = 'full'
        
    elif getType == 'small':
        for x in oldData:
            if type(oldData[x]) == dict:
                for i in oldData[x]:
                    if TMP[x][i] == oldData[x][i]:
                        TMP[x].pop(i)
            else:
                if 'type' in oldData:
                    if TMP[x] == oldData[x]:
                        TMP.pop(x)
                else:
                    TMP['type'] = 'full'
                    emit('data', json.dumps(TMP))
                    return
        TMP['type'] = 'small'
    emit('data', json.dumps(TMP))
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

@flaskapp.route("/reset")
def reset():
    DATA['state']['error'] = False
    DATA['state']['errorActive'] = False
    return redirect(url_for('home'))


# test
@flaskapp.route("/info")
def info():
    return render_template('infoPage.html', test='hoi')
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
