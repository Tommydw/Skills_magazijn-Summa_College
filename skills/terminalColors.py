# colors in terminal 
class colors:
    '''Colors class:
    Reset all colors with colors.reset
    Two subclasses fg for foreground and bg for background.
    Use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    Also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    blink = '\033[5m' # 6m

    class forground:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'

    class background:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

def server_log(text): # orange
    print(colors.reset + colors.forground.orange + 'Server: ' + text + colors.reset)
    
def server_info(text): # green
    print(colors.reset + colors.forground.green + 'Server: ' + text + colors.reset)

def server_error(text): # red blink bold
    print(colors.reset + colors.forground.red + colors.blink + colors.bold + 'Server: ' + text + colors.reset)

def io_log(text): # blue
    print(colors.reset + colors.forground.lightblue + 'IO log: ' + colors.reset + text)


