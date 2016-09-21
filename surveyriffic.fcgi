#!/usr/bin/env python3.4

import traceback
import logging
import sys
#sys.path.insert(0, "/home/perigen/surveyriffic")

#try:

# run it via virtualenv:
activate_this = "/home/perigen/surveyriffic/.env/bin/activate_this.py"

exec(compile(open(activate_this, "rb").read(), activate_this, 'exec'))

# now import the application
import bottle
# see: <http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend>
app = bottle.default_app()
# see: <https://github.com/Kozea/flipflop>
from flipflop import WSGIServer

if __name__ == '__main__':
    WSGIServer(app).run()
