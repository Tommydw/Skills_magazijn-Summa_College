from skills import SOCKET_INFO, routes, rpi
from skills.terminalColors import server_info, server_log, server_error, colors
from data import DATA, PINNEN, TEMP
import time, os, platform

# init voor orderUitvoeren
cilinder_uit_tijd   = 2 #sec ### pas deze aan om de cilinder slag aan te passen ###
cilinder_in_tijd    = 1 #sec
band_off_delay      = 5 #sec

def orderUitvoeren():  
    # bij een nieuw order
    if DATA['state']['order']['orderActive']:
        '''### cilinders ###'''
        if not TEMP['order_compleet']:
            now_time = time.time()
            # eerste keer de tijd vast leggen
            if not TEMP['running']:
                TEMP['running'] = True
                TEMP['start_time'] = time.time()
            # als de tijd + cilinder uit + cilinder in delay
            if TEMP['start_time'] >=  now_time - cilinder_uit_tijd - cilinder_in_tijd:
                # als de tijd + cilinder uit delay
                if TEMP['start_time'] >= now_time - cilinder_uit_tijd:
                    '''### stap 1 ###''' 
                    if TEMP['write_high']:
                        # eenmalig uitvoeren
                        TEMP['write_high'] = False
                        if TEMP['blokjes_op_band'] == -1: # als er geen blokjes op de band staan
                            TEMP['blokjes_op_band'] = 1
                        else: # als er al minimaal één blokje op de band staat
                            TEMP['blokjes_op_band'] += 1
                            
                        # zet de cilinder aan
                        if DATA['state']['order']['kleur'] == 'rood': 
                            rpi.write('cil1', True)
                        elif DATA['state']['order']['kleur'] == 'zwart': 
                            rpi.write('cil2', True)
                        elif DATA['state']['order']['kleur'] == 'zilver': 
                            rpi.write('cil3', True)
                        server_log('Aantal blokjes nu: {0}'.format(TEMP['blokjes_op_band']))    
                        magazijn.leegCheck() # als de sensor geen blokjes meer ziet, is er nog één mogelijkheid
                else:
                    '''### stap 2 ###'''
                    # zet de cilinders uit
                    if DATA['state']['order']['kleur'] == 'rood': 
                        rpi.write('cil1', False)
                    elif DATA['state']['order']['kleur'] == 'zwart': 
                        rpi.write('cil2', False)
                    elif DATA['state']['order']['kleur'] == 'zilver':
                        rpi.write('cil3', False)
                    
                    # reset en disable cilinder loop
                    TEMP['write_high'] = TEMP['order_compleet'] = True
                    TEMP['running'] = False
                    TEMP['start_time'] = 0
            else: 
                '''### stap 3 fallback ###'''
                # hier kom je als het goed is niet, anders reset loop 
                TEMP['running'] = False
                TEMP['write_high'] = True
                TEMP['start_time'] = 0
        
        # slave
        if not DATA['state']['master']:
            # kijken of de PLC een sigaal heeft gegeven 
            if DATA['io']['PLCbusy'] and DATA['io']['PLCactief'] and not TEMP['detectPLC'] and TEMP['detectBokje']:
                TEMP['detectPLC'] = True
                
        # MASTER = als er een blokje is gedetecteerd
        # SLAVE = als er een blokje is gedetecteerd en een PLC signaal heeft gekeregen
        if (not DATA['state']['master'] and TEMP['detectPLC'] and TEMP['detectBokje']) or (DATA['state']['master'] and TEMP['detectBokje']):
            # reset detect voorwaarden
            TEMP['detectBokje'] = TEMP['detectPLC'] = False
            
            # order klaar, volgende mag besteld worden
            DATA['state']['order']['orderActive'] = TEMP['order_compleet'] = False 
            
            # dan reset de order naar default
            rpi.write('check', False)
            rpi.write('deksel', False)
            rpi.write('muntje', False)
            rpi.write('Kleur1', False)
            rpi.write('Kleur2', False)
            DATA['state']['order']['kleur'] = ''
            DATA['state']['order']['deksel'] = False
            DATA['state']['order']['muntje'] = False
    else:
        '''### stap 3 ###'''
        TEMP['running'] = False
        TEMP['write_high'] = True
        TEMP['start_time'] = 0


    '''### Lopende band ###'''        
    # als er een blokje op de band is 
    if TEMP['blokjes_op_band'] > 0:
        Time = time.time()
        
        # als de motor uit staat
        if not DATA['io']['motor']: 
            rpi.write('motor', True)
        
        # als er een blokje gedetecteerd is
        if not DATA['io']['eind']:
            if not TEMP['detect']: # eenmalig
                TEMP['detect'] = True
                '''### onderstaand was voor stand-alone ###'''
                # TEMP['end_time'] = Time # (her)start timer om de band uit te schakelen
                # DATA['state']['order']['orderActive'] = TEMP['order_compleet'] = False # order klaar, volgende mag besteld worden
        # als de sensor weer laag gaat
        elif TEMP['detect']:
            TEMP['end_time'].append(Time) # (her)start timer om de band uit te schakelen
            TEMP['detectBokje'] = True
            TEMP['detect'] = False # reset eenmalig proces
            
        # timer om de band uit te schakelen
        # if TEMP['end_time'] <= Time - band_off_delay and not TEMP['end_time'] == 0 and TEMP['end_time'] >= Time - band_off_delay - 0.1:
        for endTims in TEMP['end_time']:
            if endTims <= Time - band_off_delay and endTims >= Time - band_off_delay - 0.1:
                TEMP['blokjes_op_band'] -= 1
                TEMP['end_time'].pop(TEMP['end_time'].index(endTims)) # reset start timer
                server_log('Aantal blokjes nu: {0}'.format(TEMP['blokjes_op_band']))
    
    # als er geen blokjes op de band zijn, maar de moter wel aan is
    elif DATA['io']['motor'] and TEMP['blokjes_op_band'] == 0:
        # reset timer en zet de motor uit
        TEMP['blokjes_op_band'] = -1
        rpi.write('motor', False)          
            
class magazijn():
    def Controle():
        # controleren of de magazijnen bijna leeg zijn
        # als de sensor geen blokje ziet, zit er 1 op minder blokjes in (warning)
        # (frontend warning)
        # rood
        if DATA['io']['mag1'] and DATA['state']['stock']['mag1'] == 2:
            DATA['state']['stock']['mag1'] = 1
            server_info('Magazijn 1 is bijna leeg (rood)')
        elif not DATA['io']['mag1']:
            DATA['state']['stock']['mag1'] = 2
            if not DATA['state']['order']['orderActive'] and DATA['io']['cil1']:
                rpi.write('cil1', False)
        # zwart
        if DATA['io']['mag2'] and DATA['state']['stock']['mag2'] == 2:
            DATA['state']['stock']['mag2'] = 1
            server_info('Magazijn 2 is bijna leeg (zwart)')
        elif not DATA['io']['mag2']:
            DATA['state']['stock']['mag2'] = 2
            if not DATA['state']['order']['orderActive'] and DATA['io']['cil2']:
                rpi.write('cil2', False)
        # zilver
        if DATA['io']['mag3'] and DATA['state']['stock']['mag3'] == 2:
            DATA['state']['stock']['mag3'] = 1
            server_info('Magazijn 3 is bijna leeg (zilver)')
        elif not DATA['io']['mag3']:
            DATA['state']['stock']['mag3'] = 2
            if not DATA['state']['order']['orderActive'] and DATA['io']['cil3']:
                rpi.write('cil3', False)

    def leegCheck():
        # als de sensor geen blokjes meer ziet, is er nog één mogelijkheid, daarna zijn ze op
        # (frontend warning)
        # rood
        if DATA['state']['stock']['mag1'] == 1 and DATA['state']['order']['kleur'] == 'rood':
            DATA['state']['stock']['mag1'] = 0
            server_error("Magazijn 1 is leeg! (rood)")
        # zwart
        if DATA['state']['stock']['mag2'] == 1 and DATA['state']['order']['kleur'] == 'zwart':
            DATA['state']['stock']['mag2'] = 0
            server_error("Magazijn 2 is leeg! (zwart)")
        # zilver
        if DATA['state']['stock']['mag3'] == 1 and DATA['state']['order']['kleur'] == 'zilver':
            DATA['state']['stock']['mag3'] = 0
            server_error("Magazijn 3 is leeg! (zilver)")

    def leegState():
        if DATA['state']['stock']['mag1'] == 0 and not DATA['io']['cil1']:
            rpi.write('cil1', True)
        if DATA['state']['stock']['mag2'] == 0 and not DATA['io']['cil2']:
            rpi.write('cil2', True)
        if DATA['state']['stock']['mag3'] == 0 and not DATA['io']['cil3']:
            rpi.write('cil3', True)




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
                        if time.time() - user[1] > 30:
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
                    if pin.__contains__('PLC'):
                        DATA['io'][pin] = rpi.read(pin, overwrite=True)
                    else:
                        DATA['io'][pin] = rpi.read(pin, overwrite=DATA['state']['devMode'])
            
            # zet error aan als een deurtje open gaat 
            if (((not DATA['io']['mcp1Noodstop'] or not DATA['io']['mcp2Noodstop']) and not DATA['state']['overRideMode']) 
            or (not DATA['state']['master'] and not DATA['io']['PLCerror'])) and not DATA['state']['errorActive'] and OS == 'Linux':
                DATA['state']['errorActive'] = True
                error_time = time.time()
            elif (DATA['io']['mcp1Noodstop'] and DATA['io']['mcp2Noodstop'] and not DATA['state']['overRideMode']) and not (not DATA['state']['master'] and not DATA['io']['PLCerror']): DATA['state']['errorActive'] = False
            if time.time() - error_time > 0.05 and DATA['state']['errorActive']:
                DATA['state']['error'] = True
            
            # Set time
            DATA['time'] = time.time()
            DATA['state']['cpu'] = list(os.getloadavg()) if linux else 'Windows'

            # stop event
            if DATA['state']['error'] == True and not DATA['state']['devMode']:
                rpi.write('motor', PINNEN['motor']['state'], override=True, log=False)

            # disable override mode
            if not DATA['state']['devMode'] and DATA['state']['overRideMode']:
                DATA['state']['overRideMode'] = False
                server_log('Noodstop override mode False')

            orderUitvoeren()
            magazijn.Controle()
            magazijn.leegState()