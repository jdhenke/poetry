import os, sys, cherrypy
import simplejson as json

class Server(object):

  _cp_config = {'tools.staticdir.on' : True,
                'tools.staticdir.dir' : os.path.abspath(os.path.join(os.getcwd(), "www")),
                'tools.staticdir.index' : 'index.html',
                }

  def __init__(self):
    # TODO
    pass

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_edges(self, text, allNodes):
    return self.provider.get_edges(text, json.loads(allNodes))

cherrypy.config.update({'server.socket_host': '0.0.0.0', 
                        'server.socket_port': int(sys.argv[1]), 
                       }) 

cherrypy.quickstart(Server())