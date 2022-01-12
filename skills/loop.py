from skills import SOCKET_INFO, routes, rpi
from skills.terminalColors import server_info, server_log, server_error, colors
from data import DATA, PINNEN
import time, os, platform

# init voor orderUitvoeren
cilinder_uit_tijd   = 1 #sec
cilinder_in_tijd    = 1 #sec
band_off_delay      = 4 #sec
blokjes_op_band = -1
running = False
write_high = True
start_time = 0
end_time = 0
detect = True
order_compleet = False

def orderUitvoeren():
    global running
    global start_time   
    global write_high   
    global blokjes_op_band
    global end_time
    global detect
    global order_compleet
    if DATA['state']['order']['orderActive'] and not order_compleet:
        now_time = time.time()
        if not running:
            running = True
            start_time = time.time()
        if start_time >=  now_time - cilinder_uit_tijd - cilinder_in_tijd:
            if start_time >= now_time - cilinder_uit_tijd:
                # stap 1
                if write_high:
                    write_high = False
                    if blokjes_op_band == -1:
                        blokjes_op_band = 1
                    else:
                        blokjes_op_band += 1
                    if DATA['state']['order']['kleur'] == 'rood': 
                        rpi.write('cil1', True)
                    elif DATA['state']['order']['kleur'] == 'zwart': 
                        rpi.write('cil2', True)
                    elif DATA['state']['order']['kleur'] == 'zilver': 
                        rpi.write('cil3', True)
                    server_log('Aantal blokjes nu: {0}'.format(blokjes_op_band))
                    magazijnLeeg()
            else:
                # stap 2
                if DATA['state']['order']['kleur'] == 'rood': 
                    rpi.write('cil1', False)
                elif DATA['state']['order']['kleur'] == 'zwart': 
                    rpi.write('cil2', False)
                elif DATA['state']['order']['kleur'] == 'zilver':
                    rpi.write('cil3', False)
                write_high = order_compleet = True
                running = False
                if DATA['state']['master']:
                    rpi.write('deksel', False)
                    rpi.write('muntje', False)
                    rpi.write('Kleur1', False)
                    rpi.write('Kleur2', False)
                    DATA['state']['order']['kleur'] = ''
                    DATA['state']['order']['deksel'] = False
                    DATA['state']['order']['muntje'] = False
        else: 
            #stap 3
            running = False
            write_high = True
            start_time = 0
    else:
        running = False
        write_high = True
        start_time = 0
        
    if blokjes_op_band > 0:
        Time = time.time()
        if not DATA['io']['motor']:
            rpi.write('motor', True)
        if not DATA['io']['eind']:
            if detect:
                end_time = Time
                DATA['state']['order']['orderActive'] = order_compleet = False
                detect = False
        else:
            detect = True
        if end_time <= Time - band_off_delay and not end_time == 0 and end_time >= Time - band_off_delay - 0.1:
            blokjes_op_band -= 1
            end_time = 0
            server_log('Aantal blokjes nu: {0}'.format(blokjes_op_band))

    elif DATA['io']['motor'] and blokjes_op_band == 0:
        blokjes_op_band = -1
        rpi.write('motor', False)
            

def magazijnControle():
    if DATA['io']['mag1'] and DATA['state']['stock']['mag1'] == 2:
        DATA['state']['stock']['mag1'] = 1
        server_info('Magazijn 1 is bijna leeg (zilver)')
    elif not DATA['io']['mag1']:
        DATA['state']['stock']['mag1'] = 2

    if DATA['io']['mag2'] and DATA['state']['stock']['mag2'] == 2:
        DATA['state']['stock']['mag2'] = 1
        server_info('Magazijn 2 is bijna leeg (zwart)')
    elif not DATA['io']['mag2']:
        DATA['state']['stock']['mag2'] = 2

    if DATA['io']['mag3'] and DATA['state']['stock']['mag3'] == 2:
        DATA['state']['stock']['mag3'] = 1
        server_info('Magazijn 3 is bijna leeg (rood)')
    elif not DATA['io']['mag3']:
        DATA['state']['stock']['mag3'] = 2

def magazijnLeeg():
    if DATA['state']['stock']['mag1'] == 1 and DATA['state']['order']['kleur'] == 'zilver':
        DATA['state']['stock']['mag1'] = 0
        server_error("Magazijn 1 is leeg! (zilver)")

    if DATA['state']['stock']['mag2'] == 1 and DATA['state']['order']['kleur'] == 'zwart':
        DATA['state']['stock']['mag2'] = 0
        server_error("Magazijn 2 is leeg! (zwart)")

    if DATA['state']['stock']['mag3'] == 1 and DATA['state']['order']['kleur'] == 'rood':
        DATA['state']['stock']['mag3'] = 0
        server_error("Magazijn 3 is leeg! (rood)")


class loop:
    def run():
        server_info('Running side loop')
        OS = platform.system()
        error_time = loopTime = time.time()
        linux = True if platform.system() == 'Linux' else False
        while True:
            # Blink led in loop
            # knipper sneller als de loadAVG hoger is dan 1.5
            if linux and os.getloadavg()[0] > 1.5:
                blinkTime = 1/4 #sec
            else:
                blinkTime = 1/2 #sec
                
            if time.time() - loopTime > blinkTime:
                # laat de led knipperen
                rpi.toggle_loop_run()
                # verwijder user als deze niet actief is
                try:
                    for user in SOCKET_INFO:
                        if time.time() - user[1] > 60:
                            SOCKET_INFO.pop(SOCKET_INFO.index(user))
                            server_log('User {0} '.format(user[0]) + colors.forground.red + colors.blink + 'removed' + colors.reset)
                except:
                    server_error('User not found in actief users')
                loopTime = time.time()
            
            # write error pin
            rpi.write('error', DATA['state']['error'], override = True, log=False)
            
            # read GPIO    
            for pin in PINNEN:
                if PINNEN[pin]['direction'] == 'input':
                    DATA['io'][pin] = rpi.read(pin, overwrite=DATA['state']['devMode'])
            
            # zet error aan als een deurtje open gaat 
            if (not DATA['io']['mcp1Noodstop'] or not DATA['io']['mcp2Noodstop']) and not DATA['state']['errorActive'] and OS == 'Linux':
                DATA['state']['errorActive'] = True
                error_time = time.time()
            elif DATA['io']['mcp1Noodstop'] and DATA['io']['mcp2Noodstop']: DATA['state']['errorActive'] = False
            if time.time() - error_time > 0.05 and DATA['state']['errorActive']:
                DATA['state']['error'] = True
            
            # Set time
            DATA['time'] = time.time()
            DATA['state']['cpu'] = list(os.getloadavg()) if linux else 'Windows'

            # stop event
            if DATA['state']['error'] == True and not DATA['state']['devMode']:
                rpi.write('motor', PINNEN['motor']['state'], override=True, log=False)

            orderUitvoeren()
            magazijnControle()