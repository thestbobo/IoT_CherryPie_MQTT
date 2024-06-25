import cherrypy

from SWLab1.es1 import TemperatureConverter

if __name__ == '__main__':
    cherrypy.quickstart(TemperatureConverter())