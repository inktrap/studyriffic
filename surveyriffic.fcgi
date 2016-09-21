#!/usr/bin/env python3.4

import traceback
import logging
import sys
sys.path.insert(0, "/home/perigen/surveyriffic")

#try:

# run it via virtualenv:
#activate_this = "/home/perigen/surveyriffic/.env/bin/activate_this.py"
#exec(compile(open(activate_this, "rb").read(), filename, 'exec')

from flipflop import WSGIServer
# see: <http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend>
app = bottle.default_app()

if __name__ == '__main__':
    WSGIServer(app).run()
    #WSGIServer(run(server='flup')).run()

#except Exception as e:
#    logging.error(traceback.format_exc())
#    # Logs the error appropriately. 
