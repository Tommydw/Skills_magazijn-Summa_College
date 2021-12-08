# import raspberry pi GPIO 
# import RPi.GPIO as gpio
from RPiMCP23S17.MCP23S17 import MCP23S17, GPIO as gpio
from skills.terminalColors import io_log, colors, server_error, server_info, server_log
import spidev
from data import DATA, PINNEN

class rpi:
    # setup all io's
    def setup():
        try:
            # start GPIO communicatie
            server_log('Setup RPI GPIO')
            try:
                gpio.setwarnings(False)
                gpio.setmode(gpio.BOARD) 
                DATA['state']['gpio'] = True
            except:
                DATA['state']['gpio'] = False
                server_error('Error while setting up PI GPIO')
                
            # have to slow down the SPI bus for better communication
            spi = spidev.SpiDev()
            spi.open(0,0)
            spi.max_speed_hz = 5000000   
            server_info('SPI slow down to -> 5MHz')

            # start MCP1
            server_log('Setup MCP1')    
            try:
                global mcp1
                mcp1 = MCP23S17(device_id=0x00)
                mcp1.open() 
                DATA['state']['mcp1'] = True
            except:
                DATA['state']['mcp1'] = False
                server_error('Error while setting up MCP1')
            
            # start MCP2
            server_log('Setup MCP2')
            try:
                global mcp2
                mcp2 = MCP23S17(device_id=0x01)
                mcp2.open()
                DATA['state']['mcp2'] = True
            except:
                DATA['state']['mcp2'] = False
                server_error('Error while setting up MCP2')
            
            # stel de GPIO pinnen in als in of output
            io_log('GPIO pinnen:')
            for pin in PINNEN:
                # define inputs                
                if PINNEN[pin]['direction'] == 'input':
                    if 'pull' in PINNEN[pin]:
                        # set input on PI	
                        if PINNEN[pin]['module'] == 'pi':
                            gpio.setup(PINNEN[pin]['pin'], gpio.IN, pull_up_down=(
                                gpio.PUD_DOWN if PINNEN[pin]['pull'] == 'down' else (
                                gpio.PUD_UP if PINNEN[pin]['pull'] == 'up' else gpio.PUD_DOWN))) # define as input and set pullup/down
                        # set input on MCP1
                        elif PINNEN[pin]['module'] == 'mcp1':
                            mcp1.setDirection(PINNEN[pin]['pin'], mcp1.DIR_INPUT) # define as input
                            mcp1.setPullupMode(PINNEN[pin]['pin'],(mcp1.PULLUP_DISABLED if PINNEN[pin]['pull'] == 'down' else (
                                                                    mcp1.PULLUP_ENABLED if PINNEN[pin]['pull'] == 'up' else mcp1.PULLUP_DISABLED))) # set pullup/down
                        # set input on MCP2
                        elif PINNEN[pin]['module'] == 'mcp2':
                            mcp2.setDirection(PINNEN[pin]['pin'], mcp1.DIR_INPUT) # define as input
                            mcp2.setPullupMode(PINNEN[pin]['pin'],(mcp1.PULLUP_DISABLED if PINNEN[pin]['pull'] == 'down' else (
                                                                    mcp1.PULLUP_ENABLED if PINNEN[pin]['pull'] == 'up' else mcp1.PULLUP_DISABLED))) # set pullup/down
                    # generate exception when IO list is corrupt
                    else: 
                        raise Exception(' "pull" is not defind in PINNEN - {0}'.format(pin))
                
                # define outputs
                elif PINNEN[pin]['direction'] == 'output':
                    # set output on PI
                    if PINNEN[pin]['module'] == 'pi':    
                        gpio.setup(PINNEN[pin]['pin'], gpio.OUT) # define output
                        gpio.output(PINNEN[pin]['pin'], (gpio.LOW if PINNEN[pin]['state'] == 'low' else 
                                                         (gpio.HIGH if PINNEN[pin]['state'] == 'high' else gpio.LOW))) # write state to output
                    # set output on MCP1	
                    elif PINNEN[pin]['module'] == 'mcp1':
                        mcp1.setDirection(PINNEN[pin]['pin'], mcp1.DIR_OUTPUT) # define output
                        mcp1.digitalWrite(PINNEN[pin]['pin'], (mcp1.LEVEL_LOW if PINNEN[pin]['state'] == 'low' else 
                                                                (mcp1.LEVEL_HIGH if PINNEN[pin]['state'] == 'high' else mcp1.LEVEL_LOW))) # write state to output
                    # set output on MCP2
                    elif PINNEN[pin]['module'] == 'mcp2':
                        mcp2.setDirection(PINNEN[pin]['pin'], mcp1.DIR_OUTPUT) # define output
                        mcp2.digitalWrite(PINNEN[pin]['pin'], (mcp1.LEVEL_LOW if PINNEN[pin]['state'] == 'low' else 
                                                                (mcp1.LEVEL_HIGH if PINNEN[pin]['state'] == 'high' else mcp1.LEVEL_LOW))) # write state to output
                else:
                    raise Exception('Error while trying to define pin {0}'.format(pin))
  
                # print pin status
                # io_log('Pin number {0} has name "{1}" and is an {2} on device {3}'.format(str(PINNEN[pin]['pin']), pin, PINNEN[pin]['direction'], PINNEN[pin]['module']))
                io_log('Pin number {0} has name "{1}" and is an {2} on device {3}'.format(
                    PINNEN[pin]['pin'], 
                    colors.forground.yellow + pin + colors.reset, 
                    colors.forground.lightred + PINNEN[pin]['direction'] + colors.reset, 
                    colors.forground.lightcyan + PINNEN[pin]['module'] + colors.reset))
                    
            # script is aan het starten 
            # gpio.output(PINNEN["io_active"]['pin'], gpio.HIGH) 
            # rpi.write('io_active', 1)
            return True
        except:
            return False
        
    # write function
    def write(pin, state, override=False, log=True):
        if not DATA['state']['error'] or override:
            # print if the function had been override
            if override and log: io_log(colors.bold + 'override')
            if pin in PINNEN:
                
                # log pin state
                if log: io_log('Set pin ' + colors.forground.yellow + '{0} {1}'.format(pin, colors.forground.lightgreen + 'LOW' + colors.reset if state == 'low'.lower() or state == 0 else 
                                                (colors.forground.lightred + 'HIGH' + colors.reset if state == 'high'.lower() or state == 1 else 
                                                colors.reset + colors.background.red + colors.forground.lightgrey + colors.blink + 'ERROR' + colors.reset)) + colors.reset)
                # set pin LOW
                if state == 'low'.lower() or state == 0:
                    if PINNEN[pin]['module'] == 'pi':
                        gpio.output(PINNEN[pin]['pin'], gpio.LOW) # pull low
                    elif PINNEN[pin]['module'] == 'mcp1':
                        mcp1.digitalWrite(PINNEN[pin]['pin'], mcp1.LEVEL_LOW) # write state to output
                    elif PINNEN[pin]['module'] == 'mcp2':
                        mcp2.digitalWrite(PINNEN[pin]['pin'], mcp1.LEVEL_LOW) # write state to output
                        # write status to data
                    DATA['io'][pin] = False
                
                # set pin HIGH       
                elif state == 'high'.lower() or state == 1:
                    if PINNEN[pin]['module'] == 'pi':
                        gpio.output(PINNEN[pin]['pin'], gpio.HIGH) # pull low
                    elif PINNEN[pin]['module'] == 'mcp1':
                        mcp1.digitalWrite(PINNEN[pin]['pin'], mcp1.LEVEL_HIGH) # write state to output
                    elif PINNEN[pin]['module'] == 'mcp2':
                        mcp2.digitalWrite(PINNEN[pin]['pin'], mcp1.LEVEL_HIGH) # write state to output
                    # write status to data
                    DATA['io'][pin] = True
            
            # log error        
            else:
                server_error('{0} state is not defined for pin "{1}"'.format(state, pin))
        else:
            server_error('cannot assing state {0} to pin "{1}" in error event'.format(state, pin))
             
    # # write to pi GPIO without logging      
    # def write_loop(pin, state):
    #     if state == 'low'.lower() or state == 0:
    #         gpio.output(PINNEN[pin]['pin'], gpio.LOW) # pull LOW
    #         # write status to data
    #         DATA['io'][pin] = False
    #     elif state == 'high'.lower() or state == 1:
    #         gpio.output(PINNEN[pin]['pin'], gpio.HIGH) # pull HIGH
    #         # write status to data
    #         DATA['io'][pin] = True
    
    # read GPIO
    def read(pin):
        if not DATA['state']['error']:
            if pin in PINNEN:
                if PINNEN[pin]['module'] == 'pi':
                    readValue = gpio.input(PINNEN[pin]['pin']) # read pin
                elif PINNEN[pin]['module'] == 'mcp1':
                    readValue = mcp1.digitalRead(PINNEN[pin]['pin'])
                elif PINNEN[pin]['module'] == 'mcp2':
                    readValue = mcp2.digitalRead(PINNEN[pin]['pin'])
                DATA['io'][pin] = True if readValue else False
                return True if readValue else False
            # log error        
            else:
                server_error('pin "{1}" is not found in IO list'.format(pin))
        return (False if PINNEN[pin]['pull'] == 'down' else True)
            
    # Toggle the loopRun LED
    def toggle_loop_run():
        rpi.write('loopRun', (not DATA['io']['loopRun']), override=True, log=False)
        rpi.write('MCP1', (not DATA['io']['MCP1']), override=True, log=False)
        rpi.write('MCP2', (not DATA['io']['MCP2']), override=True, log=False)
        # if DATA['io']['loopRun'] == True:
        #     rpi.write_loop('loopRun', False)
        # else:
        #     rpi.write_loop('loopRun', True)
        
        
    
    '''OUDE GPIO DEFINE CODE:'''
    # 'script_status':    {'pin': 26, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan na het initalizeren
    # 'io_active':        {'pin': 19, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan bij starten van script
    # 'loop_active':      {'pin': 21, 'direction': gpio.OUT, 'state': gpio.LOW},    # gaat aan bij starten van script
    # 'test':             {'pin': 13, 'direction': gpio.OUT, 'state': gpio.LOW},    # TEST pin
    # 'in':               {'pin': 16, 'direction': gpio.IN, 'pull': gpio.PUD_UP},   # TEST input pin pullup


    # # set pin on the pi 
    # if PINNEN[pin]['module'] == 'pi':
    #     if PINNEN[pin]['direction'] == gpio.IN:
    #         if 'pull' in PINNEN[pin]:
    #             gpio.setup(PINNEN[pin]['pin'], PINNEN[pin]['direction'], pull_up_down=PINNEN[pin]['pull']) # define as input and set pullup/down
    #         else: 
    #             raise Exception(' "pull" is not defind in PINNEN - {0}'.format(pin))
    #     elif PINNEN[pin]['direction'] == gpio.OUT:
    #         gpio.setup(PINNEN[pin]['pin'], PINNEN[pin]['direction']) # define output
    #         gpio.output(PINNEN[pin]['pin'], PINNEN[pin]['state']) # write state to output
    #     else:
    #         raise Exception('Error while trying to define pin {0}'.format(pin))
        
    # # set pin on MCP1
    # elif PINNEN[pin]['module'] == 'mcp1':
    #     if PINNEN[pin]['direction'] == 'input':
    #         if 'pull' in PINNEN[pin]:
    #             mcp1.setDirection(PINNEN[pin]['pin'], PINNEN[pin]['direction']) # define as input and set pullup/down
    #             mcp1.setPullupMode(PINNEN[pin]['pin'], PINNEN[pin]['pull'])
    #         else: 
    #             raise Exception(' "pull" is not defind in PINNEN - {0}'.format(pin))
    #     elif PINNEN[pin]['direction'] == 'output':
    #         mcp1.setDirection(PINNEN[pin]['pin'], PINNEN[pin]['direction']) # define output
    #         mcp1.digitalWrite(PINNEN[pin]['pin'], PINNEN[pin]['state']) # write state to output
    #     else:
    #         raise Exception('Error while trying to define pin {0}'.format(pin))
        
    # # set pin on MCP1
    # elif PINNEN[pin]['module'] == 'mcp2':
    #     if PINNEN[pin]['direction'] == 'input':
    #         if 'pull' in PINNEN[pin]:
    #             mcp2.setDirection(PINNEN[pin]['pin'], PINNEN[pin]['direction']) # define as input and set pullup/down
    #             mcp2.setPullupMode(PINNEN[pin]['pin'], PINNEN[pin]['pull'])
    #         else: 
    #             raise Exception(' "pull" is not defind in PINNEN - {0}'.format(pin))
    #     elif PINNEN[pin]['direction'] == 'output':
    #         mcp2.setDirection(PINNEN[pin]['pin'], PINNEN[pin]['direction']) # define output
    #         mcp2.digitalWrite(PINNEN[pin]['pin'], PINNEN[pin]['state']) # write state to output
    #     else:
    #         raise Exception('Error while trying to define pin {0}'.format(pin))
    # else:
    #         raise Exception('Error while trying to define pin {0}, no vallid module: {1}'.format(pin, PINNEN[pin]['module']))