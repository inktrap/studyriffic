#!/usr/bin/env python3.4

import traceback
import logging
import sys
#sys.path.insert(0, "/home/perigen/surveyriffic")

# set up logging
from os.path import expanduser
home = expanduser("~")
logging.basicConfig(filename=os.path.join(home, 'logs', 'hello-world.fcgi.log'), level=logging.DEBUG)

def app(environ, start_response):
     start_response('200 OK', [('Content-Type', 'text/html')])
     return('''<html>
     <head>
          <title>Hello World!</title>
     </head>
     <body>
          <h1>Hello world!</h1>
     </body>
</html>''')

try:
    # activate virtualenv:
    activate_this = os.path.join(home, "surveyriffic/.env/bin/activate_this.py")
    exec(compile(open(activate_this, "rb").read(), activate_this, 'exec'))

    # how to run flipflop see: <https://github.com/Kozea/flipflop>
    from flipflop import WSGIServer

    if __name__ == '__main__':
        WSGIServer(app).run()

except Exception as e:
    logging.error(e, exc_debug=True)

