from skills import routes, rpi
import time

global INPUT 
INPUT = {
    'test': 0,
    'in': 0
    # 'sec': 0
}

TMP = {
    'in': 1
}

class loop:
    
    def run():
        print('Running side loop')
        temp_time = time.time()
        # i = 0
        while True:
            temp_INPUT = INPUT.copy()
            if time.time() - temp_time > 1.0:
                temp_time = time.time()
                # print('time {0} sec'.format(i))
                # i += 1
                # if i %2 :
                #     INPUT['sec'] = not INPUT['sec']
                # print("test state = {0}".format(INPUT['test']))

            if temp_INPUT != INPUT:
                print(INPUT)
            
            _in = rpi.read('in')
            if _in != TMP['in']:
                TMP['in'] = INPUT['in'] = _in
                rpi.write('test', not INPUT['test'])
                INPUT['test'] = not _in
                


                

                


