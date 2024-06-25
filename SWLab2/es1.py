import cherrypy
import time
import json
from dataclasses import dataclass


@dataclass
class Services:
    serviceID: str
    name: str

    def __str__(self):
        return f"{self.serviceID}"

@dataclass
class Device:
    deviceID: str
    end_points: str
    resources: str
    timestamp: str

    def __str__(self):
        return f"{self.deviceID}"
    pass
@dataclass
class User:
    userID: str
    name: str
    surname: str
    email: str

    def __str__(self):
        return f"{self.userID}"

class Catalog:
    def __init__(self):
        self.devices = []
        self.users = []
        self.services = []

        self.load_data()

    @cherrypy.expose
    def index(self):
        return "Benvenuti nel Catalog"

    # Retrieves data from json file
    def load_data(self):
        with open("info.json", 'r') as json_info:
            data = json.load(json_info)
            self.devices = data.get("devices", [])
            self.users = data.get("users", [])
            self.services = data.get("services", [])

    def getDevice(self, id):
        for d in self.devices:
            if d["deviceID"] == id:
                return d
        return None

    def getService(self, id):
        for s in self.services:
            if s['serviceID'] == id:
                return s
        return None

    def getUser(self, id):
        for u in self.users:
            if u['userID'] == id:
                return u
        return None

    @cherrypy.expose
    def subscription_info(self):
        pass


    def update_data(self):
        with open("info.json", 'w') as json_info:
            data = {
                "users": self.users,
                "devices": self.devices,
                "services": self.services
            }
            json.dump(data, json_info, indent=4)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def GET(self, resource, id=None):
        if resource == "devices":
            if id is None:
                return self.devices
            elif id is not None:
                d = self.getDevice(id)
                if d is None:
                    cherrypy.response.status = 404
                    return {'error': 'device not found'}
                return d

        elif resource == "services":
            if id is None:
                return self.services
            elif id is not None:
                s = self.getService()
                if s is None:
                    cherrypy.response.status = 404
                    return {"error": "service not found"}
                return s

        elif resource == "users":
            if id is None:
                return self.users
            elif id is not None:
                u = self.getUser(id)
                if u is None:
                    cherrypy.response.status = 404
                    raise {'error': 'user not found'}
                return u
        else:
            cherrypy.response.status = 404
            return {'error': 'resource not found'}


    def POST(self, resource, args):


        pass

if __name__ == "__main__":
    cherrypy.quickstart(Catalog())
