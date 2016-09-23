#!/usr/bin/env python3.4

import traceback
import logging
import sys
import os
import os.path

# set up logging
from os.path import expandvars, expanduser
user = expandvars("$USER")
home = expanduser("~")
logging.basicConfig(filename=os.path.join('/var/www/virtual/', user, 'fcgi-logs', 'surveyriffic.fcgi.log'), level=logging.DEBUG, format='%(asctime)s %(message)s')

sys.path.insert(0, os.path.join(home, "surveyriffic"))

try:
    # activate virtualenv:
    filename = os.path.join(home, "surveyriffic/.env/bin/activate_this.py")
    exec(compile(open(filename, "rb").read(), filename, 'exec'), dict(__file__=filename))
    #exec(compile(open(filename, "rb").read(), filename, 'exec'))


    # now import bottle and then the application
    import bottle

    # <http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend>
    # but default_app() is deprecated since 0.8, see:
    # <https://github.com/bottlepy/bottle/blob/7fad46cd036986a576946fa05de79235b8dd7447/docs/changelog.rst#id125>
    app = bottle.default_app()

    # how to run flipflop see: <https://github.com/Kozea/flipflop>
    from flipflop import WSGIServer

    if __name__ == '__main__':
        WSGIServer(app).run()

except Exception as e:
    logging.error(e)

