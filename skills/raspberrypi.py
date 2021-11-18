# import raspberry pi GPIO 
import RPi.GPIO as gpio
from skills.terminalColors import io_log, colors, server_error
# define de IO pinnen
PINNEN = {
    'script_status':    {'pin': 26, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan na het initalizeren
    'io_active':        {'pin': 19, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan bij starten van script
    'loop_active':      {'pin': 21, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan bij starten van script
    'test':             {'pin': 13, 'direction': gpio.OUT, 'state': gpio.LOW},    # TEST pin
    'in':               {'pin': 16, 'direction': gpio.IN, 'pull': gpio.PUD_UP},   # TEST input pin pullup
    }

class rpi:
    def setup():
        try:
            # start GPIO communicatie
            gpio.setmode(gpio.BCM) 

            # stel de GPIO pinnen in als in of output
            io_log('GPIO pinnen:')
            for pin in PINNEN:
                if PINNEN[pin]['direction'] == gpio.IN:
                    if 'pull' in PINNEN[pin]:
                        gpio.setup(PINNEN[pin]['pin'], PINNEN[pin]['direction'], pull_up_down=PINNEN[pin]['pull']) # define as input and set pullup/down
                    else: 
                        raise Exception(' "pull" is not defind in PINNEN - {0}'.format(pin))
                elif PINNEN[pin]['direction'] == gpio.OUT:
                    gpio.setup(PINNEN[pin]['pin'], PINNEN[pin]['direction']) # define output
                    gpio.output(PINNEN[pin]['pin'], PINNEN[pin]['state']) # write state to output
                else:
                    raise Exception('Error while trying to define pin {0}'.format(pin))
                
                # print pin status
                io_log('Pin number {0} has name {1} and is an {2}'.format(str(PINNEN[pin]['pin']), pin, 'output' if PINNEN[pin]['direction'] == gpio.OUT else 'input'))
                    
            # script is aan het starten 
            # gpio.output(PINNEN["io_active"]['pin'], gpio.HIGH) 
            rpi.write('io_active', 1)
            return True
        except:
            return False

    def write(pin, state):
        io_log('Set pin ' + colors.forground.yellow + '{0} {1}'.format(pin, colors.forground.lightgreen + 'LOW' + colors.reset if state == 'low'.lower() or state == 0 else 
                                        (colors.forground.lightred + 'HIGH' + colors.reset if state == 'high'.lower() or state == 1 else 
                                         colors.reset + colors.background.red + colors.forground.lightgrey + colors.blink + 'ERROR' + colors.reset)) + colors.reset)
        if state == 'low'.lower() or state == 0:
            gpio.output(PINNEN[pin]['pin'], gpio.LOW) # pull low
        elif state == 'high'.lower() or state == 1:
            gpio.output(PINNEN[pin]['pin'], gpio.HIGH) # pull high
        else:
            server_error('{0} state is not defined for pin "{1}"'.format(state, pin))
    
    def read(pin):
        return gpio.input(PINNEN[pin]['pin']) # read pin
            