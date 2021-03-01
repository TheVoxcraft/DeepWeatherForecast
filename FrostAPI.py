import json
import datetime
import requests

class FrostApiCaller:
    
    def __init__(self):
        self.config = self.loadConfig("./frostmet-api.conf")
        self.clientid = self.config['clientid']
        self.secret = self.config['secret']
        self.baseurl = self.config['api']

    def loadConfig(self, filename):
        with open(filename) as fo:
            return json.load(fo)

    def get_last_hour(self, station="SN18700", query=None):
        if query == None:
            query = {'sources':station, 'referencetime':'latest', 'elements' : 'air_temperature,wind_speed_of_gust,max(wind_speed PT1H),max_wind_speed(wind_from_direction PT1H)', 'timeresolutions':'PT1H'}
        else:
            query['sources'] = station
        response = requests.get(f'{self.baseurl}/observations/v0.jsonld', params=query, headers={'Authorization' : 'Basic M2E4MTY1MjMtOWM2Yy00ZmU4LTg2YjktYTkwNGNlNDYxZTAxOg=='})
        return response.json()['data']
    
    def get_last_hours(self, _hours, station="SN18700", query=None):
        if query == None:
            query = {'sources':station, 'elements' : 'air_temperature,max(wind_speed_of_gust PT1H),max(wind_speed PT1H),max_wind_speed(wind_from_direction PT1H)', 'timeresolutions':'PT1H'}
        else:
            query['sources'] = station
        
        endpoint = datetime.datetime.now()
        startpoint = endpoint - datetime.timedelta(hours=_hours)
        query['referencetime'] = startpoint.isoformat().split(":")[0]+"/"+endpoint.isoformat().split(":")[0]

        response = requests.get(f'{self.baseurl}/observations/v0.jsonld', params=query, headers={'Authorization' : 'Basic M2E4MTY1MjMtOWM2Yy00ZmU4LTg2YjktYTkwNGNlNDYxZTAxOg=='})
        return response.json()
    



if __name__ == '__main__':
    frost = FrostApiCaller()
    print(frost.get_last_hours(2))
