from skills import routes
import time
global INPUT 
INPUT = {
    'test': 0,
    'state': 0,
    'sec': 0
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

