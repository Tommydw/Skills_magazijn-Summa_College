# import raspberry pi GPIO 
import RPi.GPIO as gpio
# define de IO pinnen
PINNEN = {
    'status': {'pin': 26, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan na het initalizeren
    'active': {'pin': 19, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan bij starten van script
    'test':   {'pin': 13, 'direction': gpio.OUT, 'state': gpio.LOW},    # test pin
    'in':  {'pin': 16, 'direction': gpio.IN, 'pull': gpio.PUD_UP},   # test input pin pullup
    }

class rpi:
    def setup():
        try:
            # start GPIO comunicatie
            gpio.setmode(gpio.BCM) 

            # stel de GPIO pinnen in als in of output
            print('GPIO pinnen:')
            for pin in PINNEN:
                if 'pull' in PINNEN[pin] and PINNEN[pin]['direction'] == gpio.IN:
                    gpio.setup(PINNEN[pin]['pin'], PINNEN[pin]['direction'], pull_up_down=PINNEN[pin]['pull'])
                else:
                    gpio.setup(PINNEN[pin]['pin'], PINNEN[pin]['direction'])
                
                print('Pin nr. {0} has name {1} and is an {2}'.format(str(PINNEN[pin]['pin']), pin, 'output' if PINNEN[pin]['direction'] == gpio.OUT else 'input'))

                # stel de output laag
                if PINNEN[pin]['direction'] == gpio.OUT: 
                    gpio.output(PINNEN[pin]['pin'], PINNEN[pin]['state']) 
                    
            # script is aan het starten 
            # gpio.output(PINNEN["active"]['pin'], gpio.HIGH) 
            rpi.write('active', 1)
            return 1
        except:
            return 0

    def write(pin, state):
        print('Set pin {0} {1}'.format(pin, state))
        if state == 'low'.lower() or state == 0:
            gpio.output(PINNEN[pin]['pin'], gpio.LOW)
        elif state == 'high'.lower() or state == 1:
            gpio.output(PINNEN[pin]['pin'], gpio.HIGH)
    
    def read(pin):
        return gpio.input(PINNEN[pin]['pin'])
            