from flask import Flask
import platform

print("Running on {0}".format('Linux' if platform.system() == 'Linux' else 'Windows'))


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
# flaskapp.secret_key = "6791611bb0b13cE1c675dfde280ba245"


# enable routes
from skills import routes
from skills.leon.routes import LEON
flaskapp.register_blueprint(LEON, url_prefix='/leon')

# init compleet
print('Init completed')
rpi.write('status', 1)