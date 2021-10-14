from flask import Flask

flaskapp = Flask(__name__, template_folder='Templates')
# flaskapp.secret_key = "6791611bb0b13cE1c675dfde280ba245"

# enable routes
from skills import routes

# init compleet
print('Init completed')