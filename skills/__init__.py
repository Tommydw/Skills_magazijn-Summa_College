from flask import Flask
import platform

# from skills.raspberrypi import rpi
print("Running on {0}".format('Linux' if platform.system() == 'Linux' else 'Windows'))


if platform.system() == 'Linux':
    # in_linux = True
    # from skills.raspberrypi import gpio, PINNEN, rpi
    from skills.raspberrypi import rpi
elif platform.system() == 'windows':
    from skills.windows import rpi
    # in_linux = False
else: 
    raise Exception("OS unknown")

if rpi.setup():
    pass
else:
    raise Exception("Error while loading GPIO")

flaskapp = Flask(__name__, template_folder='Templates')
# flaskapp.secret_key = "6791611bb0b13cE1c675dfde280ba245"


# enable routes
from skills import routes
from skills.leon.routes import LEON
flaskapp.register_blueprint(LEON, url_prefix='/leon')

# init compleet
print('Init completed')
# if in_linux:
    # gpio.output(PINNEN["status"]['pin'], gpio.HIGH) 
rpi.write('status', 1)