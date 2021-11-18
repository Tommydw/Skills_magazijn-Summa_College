global DATA
DATA = {
    'type': str(),
    'time': str(),
    'state': {
        'gpio': bool(),
        'mcp1': bool(),
        'mcp2': bool(),
        'error': bool()
        },
    'io': {
        'loopRun': bool(),
        'scriptRun': bool(),
        'error': bool(),
        'cil1': bool(),
        'cil2': bool(),
        'cil3': bool(),
        'motor': bool(),
        'MCP1': bool(),
        'mcp1Noodstop': bool(),
        'mag1': bool(),
        'mag2': bool(),
        'mag3': bool(),
        'eind': bool(),
        'MCP1_pi': bool(),
        'deksel': bool(),
        'muntje': bool(),
        'Kleur1': bool(),
        'Kleur2': bool(),
        'check': bool(),
        'noodstop_out': bool(),
        'MCP2': bool(),
        'mcp2Noodstop': bool(),
        'PLCactief': bool(),
        'PLCbusy': bool(),
        'PLCerror': bool(),
        'MCP2_pi': bool()
        }
}

global PINNEN
PINNEN = {
    'loopRun':      {'module': 'pi',    'pin': 18,  'pin_name': 'GPIO24',   'direction': 'output',   'state': 'low'},	    # 18 knipperd doormiddel van de loop om de seconde
    'scriptRun':    {'module': 'pi',    'pin': 22,  'pin_name': 'GPIO25',   'direction': 'output',   'state': 'low'},	    # 22 gaat aan waneer het script is gestart
    'error':        {'module': 'pi',    'pin': 19,  'pin_name': '--',   'direction': 'output',   'state': 'low'},	    # -- gaat aan waneer het script is gestart
    'cil1':         {'module': 'mcp1',  'pin': 21,  'pin_name': 'GPA0',     'direction': 'output',   'state': 'low'},	    # cilinder uit voor magazijn 1
    'cil2':         {'module': 'mcp1',  'pin': 22,  'pin_name': 'GPA1',     'direction': 'output',   'state': 'low'},	    # cilinder uit voor magazijn 2
    'cil3':         {'module': 'mcp1',  'pin': 23,  'pin_name': 'GPA2',     'direction': 'output',   'state': 'low'},	    # cilinder uit voor magazijn 3
    'motor':        {'module': 'mcp1',  'pin': 24,  'pin_name': 'GPA3',     'direction': 'output',   'state': 'low'},	    # lopendeband
    'MCP1':         {'module': 'mcp1',  'pin': 28,  'pin_name': 'GPA7',     'direction': 'output',   'state': 'low'},	    # gaat aan waneer het script is gestart
    'mcp1Noodstop': {'module': 'mcp1',  'pin': 1,   'pin_name': 'GPB0',     'direction': 'input',    'pull': 'down'},	    # noodstop (deurtje) schakakelaar HIGH
    'mag1':         {'module': 'mcp1',  'pin': 2,   'pin_name': 'GPB1',     'direction': 'input',    'pull': 'down'},	    # gaat hoog waneer er nog maar een blokje in magazijn 1 zit
    'mag2':         {'module': 'mcp1',  'pin': 3,   'pin_name': 'GPB2',     'direction': 'input',    'pull': 'down'},	    # gaat hoog waneer er nog maar een blokje in magazijn 2 zit
    'mag3':         {'module': 'mcp1',  'pin': 4,   'pin_name': 'GPB3',     'direction': 'input',    'pull': 'down'},	    # gaat hoog waneer er nog maar een blokje in magazijn 3 zit
    'eind':         {'module': 'mcp1',  'pin': 5,   'pin_name': 'GPB4',     'direction': 'input',    'pull': 'down'},	    # gaat hoog waneer het blokje aan het einde van de band is
    'MCP1_pi':      {'module': 'mcp1',  'pin': 8,   'pin_name': 'GPB7',     'direction': 'input',    'pull': 'down'},	    # gaat hoog waneer 3.3 actief is op de pi
    'deksel':       {'module': 'mcp2',  'pin': 21,  'pin_name': 'GPA0',     'direction': 'output',   'state': 'low'},	    # gaat hoog als er een deksel gewenst is
    'muntje':       {'module': 'mcp2',  'pin': 22,  'pin_name': 'GPA1',     'direction': 'output',   'state': 'low'},	    # gaat hoog als er een muntje gewenst is
    'Kleur1':       {'module': 'mcp2',  'pin': 23,  'pin_name': 'GPA2',     'direction': 'output',   'state': 'low'},	    # bit 1 van de 2 bits kleur selector
    'Kleur2':       {'module': 'mcp2',  'pin': 24,  'pin_name': 'GPA3',     'direction': 'output',   'state': 'low'},	    # bit 2 van de 2 bits kleur selector
    'check':        {'module': 'mcp2',  'pin': 25,  'pin_name': 'GPA4',     'direction': 'output',   'state': 'low'},	    # gaat hoog als de data klaar staat
    'noodstop_out': {'module': 'mcp2',  'pin': 26,  'pin_name': 'GPA5',     'direction': 'output',   'state': 'low'},	    # gaat hoog als de noodstop procodure actief is (optie)
    'MCP2':         {'module': 'mcp2',  'pin': 28,  'pin_name': 'GPA7',     'direction': 'output',   'state': 'low'},	    # gaat aan waneer het script is gestart
    'mcp2Noodstop': {'module': 'mcp2',  'pin': 1,   'pin_name': 'GPB0',     'direction': 'input',    'pull': 'down'},	    # noodstop (deurtje) schakakelaar HIGH
    'PLCactief':    {'module': 'mcp2',  'pin': 2,   'pin_name': 'GPB1',     'direction': 'input',    'pull': 'down'},	    # gaat hoog als de PLC wacht
    'PLCbusy':      {'module': 'mcp2',  'pin': 3,   'pin_name': 'GPB2',     'direction': 'input',    'pull': 'down'},	    # gaat hoog als de PLC bezig is
    'PLCerror':     {'module': 'mcp2',  'pin': 4,   'pin_name': 'GPB3',     'direction': 'input',    'pull': 'down'},	    # gaat hoog als de PLC een error heeft
    'MCP2_pi':      {'module': 'mcp2',  'pin': 8,   'pin_name': 'GPB7',     'direction': 'input',    'pull': 'down'}	    # gaat hoog waneer 3.3 actief is op de pi
}