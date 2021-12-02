from skills import routes, rpi
from skills.terminalColors import server_info, server_log, server_error
from data import DATA, PINNEN
import time
import platform
# import psutil
import os

class loop:
    def run():
        server_info('Running side loop')
        temp_time = loopTime = time.time()
        # i = 0
        while True:
            if time.time() - temp_time > 1.0:
                temp_time = time.time()
            # _in = rpi.read('in')
            # if _in != DATA['IO']['in']:
            #     TMP['in'] = INPUT['in'] = _in
            #     rpi.write('test', not INPUT['test'])
            #     INPUT['test'] = not _in
            
            # Blink led in loop
            if os.getloadavg()[0] > 1.5:
                blinkTime = 1/4 #sec
            else:
                blinkTime = 1/2 #sec
            if time.time() - loopTime > blinkTime:
                rpi.toggle_loop_run()
                # rpi.write('cil1', not DATA['io']['cil1'], log=False)
                loopTime = time.time()
                # write gpio
           


            rpi.write('error', DATA['state']['error'], override = True, log=False)
            
            # read GPIO    
            for pin in PINNEN:
                if PINNEN[pin]['direction'] == 'input':
                    DATA['io'][pin] = rpi.read(pin)
            
            if not DATA['io']['mcp1Noodstop'] or not DATA['io']['mcp2Noodstop']:
                DATA['state']['error'] = True

            # Set time
            DATA['time'] = time.time()
            DATA['state']['cpu'] = list(os.getloadavg())
            # <1.5 is ok



            # rpi.write('cil2', (DATA['io']['mag1'] or DATA['io']['mag2'] or DATA['io']['mag3'] or DATA['io']['eind']), log=False)
            # rpi.write('cil2', DATA['io']['mag1'], log=False)