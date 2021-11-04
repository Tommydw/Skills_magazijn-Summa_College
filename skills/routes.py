from flask import render_template, redirect, url_for
# from skills import flaskapp, in_linux, gpio, PINNEN
from skills import flaskapp, rpi


@flaskapp.route("/")
def home():
    return render_template('test.html', test='hoi')


# test
@flaskapp.route("/on")
def ledON():
    rpi.write('test', 1)
    return redirect(url_for('home'))

@flaskapp.route("/off")
def ledOFF():
    rpi.write('test', 0)
    return redirect(url_for('home'))