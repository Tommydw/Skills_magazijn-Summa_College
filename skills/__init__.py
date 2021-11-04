from flask import Flask
import platform
print("Running on {0}".format('Linux' if platform.system() == 'Linux' else 'Windows'))


if platform.system() == 'Linux':
    in_linux = True
    from raspberrypi import gpio, PINNEN
elif platform.system() == 'windows':
    in_linux = False

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