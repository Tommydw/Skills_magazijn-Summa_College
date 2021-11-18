from skills.terminalColors import io_log, colors
class rpi:
    def setup():
        # print('running on windows')
        return True
    
    def write(pin, state):
        io_log('Set pin ' + colors.forground.yellow + '{0} {1}'.format(pin, colors.forground.lightgreen + 'LOW' + colors.reset if state == 'low'.lower() or state == 0 else 
                                        (colors.forground.lightred + 'HIGH' + colors.reset if state == 'high'.lower() or state == 1 else 
                                         colors.reset + colors.background.red + colors.forground.lightgrey + colors.blink + 'ERROR' + colors.reset)) + colors.reset)
    def read(pin):
        #io_log('Reading pin {0}, returning 0 while running on Windows'.format(pin))
        # returning 0 while running on Windows
        return False
