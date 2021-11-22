import data
from data import DATA
from flask import render_template, Blueprint

hmi = Blueprint('hmi', __name__, static_folder='../static', template_folder='./Templates')

@hmi.route("/")
def start():
    return render_template('hmi.html', title='HMI')