from flask import Flask
from flask_socketio import SocketIO
from skills.terminalColors import server_info, server_log
import platform

server_info("Running on {0}".format('Linux' if platform.system() == 'Linux' else 'Windows'))


if platform.system() == 'Linux':
    from skills.raspberrypi import rpi
elif platform.system() == 'Windows':
    from skills.windows import rpi
else: 
    raise Exception("OS unknown")

if rpi.setup():
    pass
else:
    raise Exception("Error while loading GPIO")

flaskapp = Flask(__name__, template_folder='Templates')
# flaskapp.secret_key = "6792611bb0b13cE1c675dfde290bc245"
socket_ = SocketIO(flaskapp)
socket_.init_app(flaskapp, cors_allowed_origins=[
    "http://localhost:5000",
    'http://raspberrypi.local:5000',
    '192.168.137.1:5000'])

SOCKET_INFO = {
    'active': 0
}

# enable routes
from skills import routes
from skills.leon.routes import LEON
flaskapp.register_blueprint(LEON, url_prefix='/leon')
from skills.HMI.routes import hmi
flaskapp.register_blueprint(hmi, url_prefix='/hmi')

# init compleet
server_log('Init completed')
rpi.write('scriptRun', True)

