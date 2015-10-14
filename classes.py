__author__ = 'bhavika'
import csv

from urllib import urlencode
import json
import requests

token = requests.post('https://www.arcgis.com/sharing/rest/oauth2/token/', params={
  'f': 'json',
  'client_id': 'iSQa5eOyJ7KaS8zj',
  'client_secret': '18f9f92e343049c98a7f6b835567e8ac',
  'grant_type': 'client_credentials',
  'expiration': '1440'
})

url = 'http://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?'

routes = {}

class Route:

    start = []
    end = []
    time = 0
    distance = 0
    paths = []
    points = []

    def __init__(self, start, end):
        data = {
        'f': 'json',
        'token': token.json()['access_token'],
        'stops' : {"features":
             [{"geometry":{"x":start[0],"y":start[1]}},
              {"geometry":{"x":end[0],"y":end[1]}}]}
        }

        info = requests.post(url, params= urlencode(data))
        self.start = start
        self.end = end
        self.time = info.json()['routes']['features'][0]['attributes']['Total_TravelTime']
        self.distance = info.json()['routes']['features'][0]['attributes']['Total_Miles']
        self.paths = info.json()['routes']['features'][0]['geometry']['paths'][0]
        self.points = [start, end]


    def isFeasible(self, newPoints):
        data = {
        'findBestSequence' : 'true',
        'preserverFirstStop' : 'true',
        'preserveLastStop' : 'true',
        'returnStops' : 'true',
        'returnDirections' :'true',
        'returnRoutes' :'true',
        'f': 'json',
        'token': token.json()['access_token'],
        'stops' : {"features":
             []}
        }
        x = self.points
        x.remove(self.end)
        x.append(newPoints[0])
        x.append(newPoints[1])
        x.append(self.end)
        for i in range(0,len(x)):
            (data['stops']['features']).append({"geometry":{"x":x[i][0],"y":x[i][1]}})
        info = requests.post(url, params= urlencode(data))

        time = info.json()['routes']['features'][0]['attributes']['Total_TravelTime']
        if time - self.time < 10:
            flag = True

        return flag

    def addNewPoint(self,newPoint):
        data = {
        'findBestSequence' : 'true',
        'preserverFirstStop' : 'true',
        'preserveLastStop' : 'true',
        'returnStops' : 'true',
        'returnDirections' :'true',
        'returnRoutes' :'true',
        'f': 'json',
        'token': token.json()['access_token'],
        'stops' : {"features":
             []}
        }
        x = self.points
        x.remove(self.end)
        x.append(newPoint)
        x.append(self.end)
        for i in range(0,len(x)):
            (data['stops']['features']).append({"geometry":{"x":x[i][0],"y":x[i][1]}})
        info = requests.post(url, params= urlencode(data))
        self.time = info.json()['routes']['features'][0]['attributes']['Total_TravelTime']
        self.distance = info.json()['routes']['features'][0]['attributes']['Total_Miles']
        self.paths = info.json()['routes']['features'][0]['geometry']['paths'][0]
        # self.points.remove(self.end)
        # self.points.append(newPoint)
        # self.points.append(self.end)

    def removePoint(self,point):

        self.points.remove(point)

        data = {
        'findBestSequence' : 'true',
        'preserverFirstStop' : 'true',
        'preserveLastStop' : 'true',
        'returnStops' : 'true',
        'returnDirections' :'true',
        'returnRoutes' :'true',
        'f': 'json',
        'token': token.json()['access_token'],
        'stops' : {"features":
             []}
        }
        x = self.points
        for i in range(0,len(x)):
            (data['stops']['features']).append({"geometry":{"x":x[i][0],"y":x[i][1]}})


        info = requests.post(url, params= urlencode(data))
        self.time = info.json()['routes']['features'][0]['attributes']['Total_TravelTime']
        self.distance = info.json()['routes']['features'][0]['attributes']['Total_Miles']
        self.paths = info.json()['routes']['features'][0]['geometry']['paths'][0]


def addressToCoordinates(adr):
    info = requests.post('http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find?text=%s&f=json'% adr)
    return [info.json()['locations'][0]['feature']['geometry']['x'], info.json()['locations'][0]['feature']['geometry']['y']]


start = addressToCoordinates('Nashville')
end = addressToCoordinates('Atlanta, Georgia')

route = Route(start,end)
a = route.paths
t1 = route.time

route.addNewPoint(addressToCoordinates('Knoxville'))
b = route.paths
t2 = route.time

print t1/60
print t2/60
print (t2-t1)/60

myfile = open('vals3.csv', 'wb')
wr = csv.writer(myfile)
for elem in a:
    wr.writerow(elem)

myfile2 = open('vals4.csv', 'wb')
wr = csv.writer(myfile2)
for elem in b:
    wr.writerow(elem)


