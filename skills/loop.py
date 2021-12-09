from skills import SOCKET_INFO, routes, rpi
from skills.terminalColors import server_info, server_log, server_error, colors
from data import DATA, PINNEN
import time
import platform
# import psutil
import os

class loop:
    def run():
        server_info('Running side loop')
        OS = platform.system()
        temp_time = loopTime = time.time()
        # i = 0
        linux = True if platform.system() == 'Linux' else False
        while True:
            if time.time() - temp_time > 1.0:
                temp_time = time.time()
            # _in = rpi.read('in')
            # if _in != DATA['IO']['in']:
            #     TMP['in'] = INPUT['in'] = _in
            #     rpi.write('test', not INPUT['test'])
            #     INPUT['test'] = not _in
            
            # Blink led in loop
            if linux and os.getloadavg()[0] > 1.5:
                blinkTime = 1/4 #sec
            else:
                blinkTime = 1/2 #sec
                
            if time.time() - loopTime > blinkTime:
                rpi.toggle_loop_run()
                for user in SOCKET_INFO:
                    if time.time() - user[1] > 60:
                        SOCKET_INFO.pop(SOCKET_INFO.index(user))
                        server_log('User {0} '.format(user[0]) + colors.forground.red + colors.blink + 'removed' + colors.reset)
                loopTime = time.time()
                # write gpio
           


            rpi.write('error', DATA['state']['error'], override = True, log=False)
            
            for pin in PINNEN:
                # read GPIO    
                if PINNEN[pin]['direction'] == 'input':
                    DATA['io'][pin] = rpi.read(pin)
                # # write GPIO
                # if PINNEN[pin]['direction'] == 'output':
                #     rpi.write(pin, DATA['io'][pin], log=False)
            
            if (not DATA['io']['mcp1Noodstop'] or not DATA['io']['mcp2Noodstop']) and OS == 'linux':
                DATA['state']['error'] = True

            # Set time
            DATA['time'] = time.time()
            DATA['state']['cpu'] = list(os.getloadavg()) if linux else 'Windows'
            # <1.5 is ok

            # rpi.write('cil2', (DATA['io']['mag1'] or DATA['io']['mag2'] or DATA['io']['mag3'] or DATA['io']['eind']), log=False)
            # rpi.write('cil2', DATA['io']['mag1'], log=False)