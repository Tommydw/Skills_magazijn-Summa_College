from skills import flaskapp, rpi, socket_, SOCKET_INFO
from flask_socketio import SocketIO, emit, namespace, send, disconnect
from flask import render_template, Blueprint, request
from data import DATA, PINNEN
import json
import time
import copy

from skills.terminalColors import server_log
hmi = Blueprint('hmi', __name__, static_folder='../static', template_folder='./Templates')

# krijg socket_connect van client
@socket_.on('socket_connect')
def socket_connect():
    if not request.sid in SOCKET_INFO:
        SOCKET_INFO.append([request.sid, time.time()])
        server_log("User '{0}' verbonden".format(request.sid))
        # Stuur connected naar client
        emit('connected')
    return

# disconnect event
# TODO fix it
@socket_.on('disconnect')
def disconnecting():
    return

@socket_.on('update_user')
def update_user():
    for i in range(len(SOCKET_INFO)):
        if request.sid in SOCKET_INFO[i]:
            SOCKET_INFO[i][1] = time.time()

# get_data request handeler
@socket_.on('get_data')
def getData(oldData, getType):
    TMP = copy.deepcopy(DATA)
    if getType == 'full': 
        # stuur het voledige object DATA
        TMP['type'] = 'full'
    elif getType == 'small':
        # stuur allen wijzigingen
        for x in oldData:
            if type(oldData[x]) == dict and not x == 'users':
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
    users = []
    for user in SOCKET_INFO:
        users.append(user[0])
    TMP['users'] = users
    # Stuur data naar ALLE clients
    emit('data', json.dumps(TMP), broadcast=True)
    return



@hmi.route("/")
def start():
    return render_template('hmi.html', title='HMI')

    
@socket_.on('order')
def getOrder(order):
    server_log(str(order))
    return
    

    
@socket_.on('motor')
def motor(state):
    rpi.write('motor', state)
    return
    
@socket_.on('cil1')
def cil1(state):
    rpi.write('cil1', state)
    return
    
@socket_.on('cil2')
def cil2(state):
    rpi.write('cil2', state)
    return
    
@socket_.on('cil3')
def cil3(state):
    rpi.write('cil3', state)
    return
