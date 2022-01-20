# Skills magazijn

### **Skills project 2021/2022 leerjaar 4**
#### **Industry 4.0**

Het skills magazijn is een automatisch magazijn met een website als HMI. Op de website kan je een order plaatsen, deze wordt dan uitgevoerd en doorgevoerd via de connector die als master of slave te configureren is. Het skills magazijn sluit aan op de Festo MPS-lijnen. Het project is ook een goed voorbeeld voor *industry 4.0*

Het de documentatie over het [Slave protocol](skills/static/docs/Slave-protocol.pdf) is te vinden in `skills/static/docs/Slave-protocol.pdf`

## **Dit project is gemaakt door:**

 * **Tommy de Wever**
 * **Thijm van Lier**
 * **Leon Hulsebos**

<br>

# Info

- Hotspot SSID: `Skills_magazijn`
- Hotspot wachtwoord: `P@ssw0rd`
- Hotspot IP: `192.168.1.1`
- Hostename: `raspberrypi`

Led active gaat aan wanneer de GPIO is gestart.

Led status gaat knipper (500ms) wanneer de server is opgestart. Als de *system load* boven de 1.5 komt, gaat deze knipperen met een inderval van (250ms)


<br>


## Domein/IP toevoegen aan WebSocket
___
SocketIO moet de domein naam of ip adres weten waar de request vandaan komt, deze moeten in `skills/__init__.py` worden toegevoed. <br>
Ga naar `./skills/__init__.py` en voeg het domein naam/IP toe aan de volgende regel:<br> `socketio.init_app(flaskapp, cors_allowed_origins=["http://localhost.local:5000",`**`"PROTOCOL://DOMAIN.NAME:PORT"`**`])`

<br>


# Clean install
1. [`Hotspot maken`](#1.-Hotspot-maken)
2. [`Instaleer benodigd heden`](#2.Instaleer-benodigd-heden)
3. [`Testen`](#3.Testen)
4. [`Automatisch starten`](#4.Automatisch-starten)

<br>


## 1. Hotspot maken
________________________________________
Door onderstaande script te gebruiken word er een hotspot aangemaakt met;
* SSID: `Skills_magazijn` (**letop!** geen " ", gebruik een "_", anders werkt het niet!) 
* Wachtwoord: `P@ssw0rd` 
* Router ip: `192.168.1.1`

Dit script zorgt er voor dat er een hotspot wordt aangemaakt, maar je kan ook nog verbinding maken met een wifi netwek (met eventueel internet toegang, deze internet toegang wordt dan ook via de hotspot gedeeld) 

```
sudo ./installation/setup-network.sh --install-upgrade --ap-ssid="Skills_magazijn" --ap-password="P@ssw0rd" --ap-password-encrypt  --ap-country-code="GB" --ap-ip-address="192.168.1.1" --wifi-interface="wlan0"
```

<br>

## 2. Installeer benodigd heden
________________________________________
Installeer **Python 3.8** of hoger en gebruik onderstaande command om de benodigdheden te instaleren:<br>
```
sudo pip3 install -r requirements.txt
```

<br>

## 3. Testen
________________________________________
Run de commando ```sudo python3 run.py``` om de website te starten. Als er foutmeldingen optreden, los deze dan op. Als het script zonder foutmeldingen start en er staat *running side loop*, zal het script goed zijn gestart.

Ga dan naar de website, via de hotspot `192.168.1.1` of het IP van het magazijn, start de HMI en start *inspecteren* `F12`, ga naar *Console* en controleer of er geen foutmeldingen komen. 
Wanneer er foutmeldingen komen over dat de websocket geen verbinding kan maken, ga naar [`Domein/IP toevoegen aan WebSocket`](#Domein/IP-toevoegen-aan-WebSocket).


<br>

## 4. Automatisch starten
________________________________________
Kopieër `skills_magazijn_website.service` naar `/etc/systemd/system/`

```
sudo cp ./installation/skills_magazijn_website.service /etc/systemd/system/skills_magazijn_website.service
```

#### **let goed op dat het *PATH* van onderstaande punten goed is ingevuld**
> WorkingDirectory=`/home/pi/Skills-magazijn-summa-2022`

> ExecStart=/bin/python3 `/home/pi/Skills-magazijn-summa-2022/`run.py

<br>
<br>

Start de *systemctl*:
```
sudo systemctl start skills_magazijn_website
```
<br> 

Start de *systemctl* automatisch:
```
sudo systemctl enable skills_magaijn_website
```
<br> 

Controler de *systemctl* status. Als er problemen zijn, los deze dan op:
```
sudo systemctl status skills_magaijn_website
```
