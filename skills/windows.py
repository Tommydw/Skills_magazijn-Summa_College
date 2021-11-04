class rpi:
    def setup():
        print('running on windows')
        return 1
    
    def write(pin, state):
        print('Set pin {0} {1}'.format(pin, state))
