from os import path as op

import tornado.web
import tornadio
import tornadio.router
import tornadio.server

from view import ChatRouter

ROOT = op.dirname(__file__)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/chatroomio/index.html')

#configure the Tornado application
application = tornado.web.Application(
    [(r"/", HomeHandler), ChatRouter.route()],
    flash_policy_port = 8843,
    flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
    socket_io_port = 8011,
    #
    static_path= op.join(ROOT, "static"),
    debug= 1,
)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    tornadio.server.SocketServer(application)