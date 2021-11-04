from flask import render_template, redirect, url_for
# from skills import flaskapp, in_linux, gpio, PINNEN
from skills import flaskapp, rpi
from skills.loop import INPUT


@flaskapp.route("/")
def home():
    return render_template('test.html', test='hoi')


# test
@flaskapp.route("/on")
def ledON():
    rpi.write('test', 1)
    INPUT['test'] = True
    return redirect(url_for('home'))

@flaskapp.route("/off")
def ledOFF():
    INPUT['test'] = False
    rpi.write('test', 0)
    return redirect(url_for('home'))
