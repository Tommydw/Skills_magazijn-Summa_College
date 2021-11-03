from flask import Flask
import platform
print("Running on {0}".format('Linux' if platform.system() == 'Linux' else 'Windows'))
PINNEN = {
    'status': {'pin': 26, 'direction': gpio.OUT}, # gaat aan na het initalizeren
    'active': {'pin': 19, 'direction': gpio.OUT}  # gaat aan bij starten van script
    }

if platform.system() == 'Linux':
    in_linux = True
    import RPi.GPIO as gpio
    print('GPIO pinnen:')
    gpio.setmode(gpio.BCM)
    for pin in PINNEN:
        gpio.setup(PINNEN[pin['pin']], PINNEN[pin['direction']])
        print('Pin nr. {0} is an {1}'.format(str(PINNEN[pin['pin']]), 'output' if PINNEN[pin['direction']] == gpio.OUT else 'input'))
    gpio.output(PINNEN["active"], gpio.HIGH) 

flaskapp = Flask(__name__, template_folder='Templates')
# flaskapp.secret_key = "6791611bb0b13cE1c675dfde280ba245"


# enable routes
from skills import routes
from skills.leon.routes import LEON
flaskapp.register_blueprint(LEON, url_prefix='/leon')

# init compleet
print('Init completed')
if in_linux:
    gpio.output(PINNEN["status"], gpio.HIGH) 