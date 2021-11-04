# import raspberry pi GPIO 
import RPi.GPIO as gpio

# define de IO pinnen
PINNEN = {
    'status': {'pin': 26, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan na het initalizeren
    'active': {'pin': 19, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan bij starten van script
    'test':   {'pin': 21, 'direction': gpio.OUT, 'state': gpio.LOW}     # test pin
    }
# start GPIO comunicatie
gpio.setmode(gpio.BCM) 

# stel de GPIO pinnen in als in of output
print('GPIO pinnen:')
for pin in PINNEN:
    gpio.setup(PINNEN[pin['pin']], PINNEN[pin['direction']])
    print('Pin nr. {0} is an {1}'.format(str(PINNEN[pin['pin']]), 'output' if PINNEN[pin['direction']] == gpio.OUT else 'input'))

    # stel de output laag
    if PINNEN[pin['direction']] == gpio.OUT: 
        gpio.output(PINNEN[pin], PINNEN[pin['state']]) 
        
# script is aan het starten 
gpio.output(PINNEN["active"], gpio.HIGH) 