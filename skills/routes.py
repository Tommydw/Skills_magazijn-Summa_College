from flask import render_template, redirect, url_for, request
from skills import flaskapp, rpi
from data import DATA

@flaskapp.route("/")
def home():
    return render_template('index.html', test='hoi', title='Home page')
# info
@flaskapp.route("/info")
def info():
    return render_template('infoPage.html', test='hoi')
# test
@flaskapp.route("/test")
def test():
    return render_template('test.html', test='hoi')

@flaskapp.route("/settings")
def settings():
    return render_template('settings.html', test='hoi')
