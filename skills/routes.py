from flask import render_template, redirect, url_for, request
from skills import flaskapp, rpi
from data import DATA
from socket import gethostbyname, gethostname, gethostname
from flask_socketio import SocketIO, emit, namespace, send, disconnect
from skills import flaskapp, rpi, socket_, SOCKET_INFO
import json, time, copy
from skills.terminalColors import server_error, server_info, server_log
import subprocess

@flaskapp.route("/")
def home():
    return render_template('index.html', test='hoi', title='Home page')
# info
@flaskapp.route("/info")
def info():
    return render_template('infoPage.html', test='hoi')
# test
@flaskapp.route("/test")
def test():
    return render_template('test.html', test='hoi')

@flaskapp.route("/settings")
def settings():
    return render_template('settings.html', ipaddres=gethostbyname(gethostname()), hostname=gethostname() )

# krijg socket_connect van client
@socket_.on('socket_connect', namespace='/settings')
def socket_connect():
    if not request.sid in SOCKET_INFO:
        SOCKET_INFO.append([request.sid, time.time()])
        server_log("User '{0}' verbonden".format(request.sid))
        # Stuur connected naar client
        emit('connected')
    return

# update user, zet de huidige server tijd bij de user | user is nog actief
@socket_.on('update_user', namespace='/settings')
def update_user():
    for i in range(len(SOCKET_INFO)):
        if request.sid in SOCKET_INFO[i]:
            SOCKET_INFO[i][1] = time.time()

# get_data request handeler
@socket_.on('get_data', namespace='/settings')
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

@socket_.on('devMode', namespace='/settings')
def devMode(state):
    DATA['state']['devMode'] = state
    server_info('Developer mode {0}'.format(state))
    getData({''}, 'full')  

@socket_.on('shutdownActivate', namespace='/settings')
def shutdown():
        server_info("Shutting down...")
        server_error("Good bye")
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

@socket_.on('MasterSlave', namespace='/settings')
def MasterSlave(waardeSlave):
    if type(waardeSlave) == bool:
        DATA['state']['master'] = waardeSlave
        server_info("master = {0}".format(waardeSlave))
        getData({''}, 'full') 
    else:
        server_error("MasterSlave waarde niet bekend")

@socket_.on('hotspot', namespace='/settings')
def Hotspot(waarde):
    if type(waarde) == bool:
        DATA['state']['hotspotMode'] = waarde
        getData({''}, 'full') 
        if DATA['state']['hotspotMode']:
            server_info("Hotspot on")
            command = "/usr/bin/sudo systemctl start hostapd.service"
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        else:
            server_info("Hotspot off")
            command = "/usr/bin/sudo systemctl stop hostapd.service"
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        server_error("hotspot waarde niet bekend")
    
# error handeling
# 404
@flaskapp.route('/404')
@flaskapp.errorhandler(404)
def page_not_found(error=None):
    return render_template('error_page.html')