from skills.terminalColors import io_log, colors, server_error, server_info
import data
from data import DATA, PINNEN

class rpi:
    def setup():
        # print('running on windows')
        for pin in PINNEN:
            io_log('Pin number {0} has name "{1}" and is an {2} on device {3}'.format(
                PINNEN[pin]['pin'], 
                colors.forground.yellow + pin + colors.reset, 
                colors.forground.lightred + PINNEN[pin]['direction'] + colors.reset, 
                colors.forground.lightcyan + PINNEN[pin]['module'] + colors.reset))

        server_info('Running in Windows -- GPIO are not in use')
        return True
    
    def write(pin, state, override=False, log=True):
        if not DATA['state']['error'] or override:
            # print if the function had been override
            if override and log: io_log(colors.bold + 'override')
         
            if pin in PINNEN:
                if state == 'low'.lower() or state == 0:
                    DATA['io'][pin] = False
                elif state == 'high'.lower() or state == 1:
                    DATA['io'][pin] = True
            # log error        
            else:
                server_error('{0} state is not defined for pin "{1}"'.format(state, pin))
                
            if override and log: io_log('Set pin ' + colors.forground.yellow + '{0} {1}'.format(pin, colors.forground.lightgreen + 'LOW' + colors.reset if state == 'low'.lower() or state == 0 else 
                                            (colors.forground.lightred + 'HIGH' + colors.reset if state == 'high'.lower() or state == 1 else 
                                            colors.reset + colors.background.red + colors.forground.lightgrey + colors.blink + 'ERROR' + colors.reset)) + colors.reset)
    # def write_loop(pin, state):     
    #     if state == 'low'.lower() or state == 0:
    #         DATA['io'][pin] = False
    #     elif state == 'high'.lower() or state == 1:
    #         DATA['io'][pin] = True
    #     # log error        
    #     else:
    #         server_error('{0} state is not defined for pin "{1}"'.format(state, pin))
            
    def read(pin):
        #io_log('Reading pin {0}, returning 0 while running on Windows'.format(pin))
        # returning 0 while running on Windows
        return False
    
    def toggle_loop_run():
        rpi.write('loopRun', not DATA['io']['loopRun'], override=True, log=False)
        # if DATA['io']['loopRun'] == True:
        #     rpi.write_loop('loopRun', False)
        # else:
        #     rpi.write_loop('loopRun', True)