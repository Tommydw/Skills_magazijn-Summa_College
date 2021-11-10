# FancyBoiii2021

Skills project 2021 leerjaar 4

# Info
Debug = True
Poort = 5000
Server = local

install requirements
pip install -r requirements.txt

led active gaat aan waneer de GPIO is ingesteld
led status gaat aan waneer de server is opgestart

# Add domain
socketio does need to know the domain name.
go to ./skills/__init__.py and add the domain name in 'socketio.init_app(app, cors_allowed_origins=["DOMAIN.NAME:PORT"])'
