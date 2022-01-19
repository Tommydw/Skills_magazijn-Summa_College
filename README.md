# FancyBoiii2021
Skills project 2021/2022 leerjaar 4


# Info
* Debug = True
* Poort = 5000
* Server = local


led active gaat aan wanneer de GPIO is ingesteld.
led status knippert zodra de loop actief is, wanneer de system load boven 1.5 is, zal de led sneller gaan knipperen


# install requirements
pip install -r requirements.txt

# Add domain
SocketIO moet de domein naam/ip weten. Ga naar ./skills/__init__.py en voeg de domein naam/ip toe aan de volgende regel: ```'socketio.init_app(app, cors_allowed_origins=["http://localhost:5000", "PROTOCOOL://DOMAIN.NAME:PORT"])'```


# export naar docker
1. sudo apt update
2. sudo apt install docker-compose
2. Ga naar de bestandsfolder waar docker-compose.yml in staat.
3. sudo docker-compose up