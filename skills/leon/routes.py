from flask import render_template, Blueprint

LEON = Blueprint('LEON', __name__, static_folder='../static', template_folder='./Templates')

@LEON.route("/")
def Leon():
    return render_template('leon.html')