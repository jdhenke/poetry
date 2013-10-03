import os, sys, cherrypy

class Server(object):

  _cp_config = {'tools.staticdir.on' : True,
                'tools.staticdir.dir' : os.path.abspath(os.path.join(os.getcwd(), "www")),
                'tools.staticdir.index' : 'index.html',
                }

cherrypy.config.update({'server.socket_host': '0.0.0.0', 
                        'server.socket_port': int(sys.argv[1]), 
                       }) 

cherrypy.quickstart(Server())