from flask.templating import render_template
from skills import flaskapp, in_linux, gpio

@flaskapp.route("/")
def home():
    return render_template('test.html', test='hoi')
