from skills import routes, rpi
from skills.terminalColors import server_info, server_log, server_error
import data
from data import DATA, PINNEN
import time
import platform

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
            if time.time() - loopTime > 1.0:
                rpi.toggle_loop_run()
                loopTime = time.time()
                # write gpio

            rpi.write('error', DATA['state']['error'], override = True, log=False)
            
            # read GPIO    
            for pin in PINNEN:
                if PINNEN[pin]['direction'] == 'input':
                    DATA['io'][pin] = rpi.read(pin)
            
            # Set time
            DATA['time'] = time.time()
                


                

                


