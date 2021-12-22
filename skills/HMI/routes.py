from skills import flaskapp, rpi, socket_, SOCKET_INFO
from flask_socketio import SocketIO, emit, namespace, send, disconnect
from flask import render_template, Blueprint, request
from data import DATA, PINNEN
import json, time, copy

from skills.terminalColors import server_error, server_info, server_log
hmi = Blueprint('hmi', __name__, template_folder='./Templates')

# krijg socket_connect van client
@socket_.on('socket_connect', namespace='/hmi')
@socket_.on('socket_connect', namespace='/hmi/onderhoud')
def socket_connect():
    if not request.sid in SOCKET_INFO:
        SOCKET_INFO.append([request.sid, time.time()])
        server_log("User '{0}' verbonden".format(request.sid))
        # Stuur connected naar client
        emit('connected')
    return

# disconnect event
# TODO fix it
@socket_.on('disconnect', namespace='/hmi')
def disconnecting():
    return

# update user, zet de huidige server tijd bij de user | user is nog actief
@socket_.on('update_user', namespace='/hmi')
@socket_.on('update_user', namespace='/hmi/onderhoud')
def update_user():
    for i in range(len(SOCKET_INFO)):
        if request.sid in SOCKET_INFO[i]:
            SOCKET_INFO[i][1] = time.time()

# get_data request handeler
@socket_.on('get_data', namespace='/hmi')
@socket_.on('get_data', namespace='/hmi/onderhoud')
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


# krijg de bestelling    
@socket_.on('order', namespace='/hmi')
@socket_.on('order', namespace='/hmi/onderhoud')
def getOrder(order):
    server_log(str(order))
    DATA['state']['order']['kleur'] = order['kleur']
    DATA['state']['order']['deksel'] = order['deksel']
    DATA['state']['order']['muntje'] = order['muntje']
    DATA['state']['order']['orderActive'] = True
    getData({''}, 'full')  
    # schrijf gpio als master = True
    if DATA['state']['master']:
        rpi.write('deksel', order['deksel'])
        rpi.write('muntje', order['muntje'])
        # schrijf 01 = rood
        if order['kleur'] == 'rood':
            rpi.write('Kleur1', True)
            rpi.write('Kleur2', False)
        # schrijf 10 = zwart
        elif order['kleur'] == 'zwart':
            rpi.write('Kleur1', False)
            rpi.write('Kleur2', True)
        # schrijf 11 = zilver
        elif order['kleur'] == 'zilver':
            rpi.write('Kleur1', True)
            rpi.write('Kleur2', True)
    return
    
@socket_.on('devMode', namespace='/hmi/onderhoud')
def devMode(state):
    DATA['state']['devMode'] = state
    server_info('Developer mode {0}'.format(state))
    getData({''}, 'full')  
    
@socket_.on('toggleSate', namespace='/hmi/onderhoud')
def toggleSate(name):
    if name in DATA['io']:
        server_log('developer toggle {0}'.format(name))
        rpi.write(name, not DATA['io'][name], override=True)
    else:
        server_error('"{0}" was not found in PINNEN'.format(name))

# render HMI (home) template
@hmi.route("/")
def start():
    masterState = request.args.get('master')
    if masterState == 'jip':
        DATA['state']['master'] = True  
    elif masterState == 'nope' :
        DATA['state']['master'] = False
    return render_template('hmi.html', title='HMI')

@hmi.route("/onderhoud")
def onderhoud():
    resetSate = request.args.get('reset_error')
    if resetSate == 'jip': 
        DATA['state']['error'] = False
        DATA['state']['errorActive'] = False
        server_info('Reset error')
    return render_template('onderhoud.html',  title='Onderhoud')