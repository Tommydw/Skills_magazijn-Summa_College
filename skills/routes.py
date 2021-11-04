from flask import render_template, redirect, url_for
from skills import flaskapp, in_linux, gpio, PINNEN

@flaskapp.route("/")
def home():
    return render_template('test.html', test='hoi')


# test
@flaskapp.route("/on")
def ledON():
    if in_linux:
        gpio.output(PINNEN['test']['pin'], gpio.HIGH) 
    return redirect(url_for('home'))
    
@flaskapp.route("/off")
def ledOFF():
    if in_linux:
        gpio.output(PINNEN['test']['pin'], gpio.LOW) 
    return redirect(url_for('home'))