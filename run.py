from skills import flaskapp, rpi, socket_
import threading
import skills.loop as loop

# Run 
if __name__ == "__main__":
    threading.Thread(name='Loop', target=loop.loop.run).start()
    # flaskapp.run(debug=True, port='5000', host='0.0.0.0', use_reloader=False)
    # socket_.run(flaskapp, debug=True, port='5000', host='0.0.0.0', use_reloader=False)
    socket_.run(flaskapp, debug=False, port='80', host='0.0.0.0', use_reloader=False)
    # flaskSettings = {
    #     'host': '0.0.0.0', 
    #     'port': 5000, 
    #     'threaded': True, 
    #     'use_reloader': False, 
    #     'debug': True
    #     }