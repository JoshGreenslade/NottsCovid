import datetime
import json
import requests
from pandas import json_normalize

# Load in configuration
with open('./config/nottsConfig.json', 'r') as f:
    config = json.load(f)


class DataCtrl:
    """ A class for controlling the data and API interaction """

    def __init__(self):

        self.time_format = "%Y-%m-%d %H:%M:%S"

        self.endpoint = 'https://coronavirus.data.gov.uk/api/v1/soa?'

        self.last_updated = datetime.datetime.strptime(
            config['lastUpdated'], self.time_format)

        time_now = datetime.datetime.utcnow()
        if (time_now - self.last_updated > datetime.timedelta(days=1)):
            self.update_data()

        # Init the geojson
        with open('./data/nottsGeoJSON.json') as geofile:
            geojson = json.load(geofile)
            i = 0
            for feature in geojson["features"]:
                feature['id'] = feature['properties']['msoa01cd']
                i += 1
        self.geojson = geojson

    def update_data(self):
        """ Updates the local and stored data from the API """

        time_now = datetime.datetime.utcnow()

        config['lastUpdated'] = time_now.strftime(self.time_format)

        with open('./config/nottsConfig.json', 'w') as f:
            json.dump(config, f, indent=4)

    def get(self, filter='', structure=''):
        """ Get data from the endpoint with the given filters and structure"""

        payload = ''.join([self.endpoint, filter, structure])
        r = requests.get(payload)
        if r.status_code == 200:
            json_data = r.json()
            return json_data
        else:
            pass

    def get_data_for_area(self, area_code):
        filter = f'filters=&areaType=msoa&areaCode={area_code}'
        data = self.get(filter=filter)
        if data is not None:
            df = json_normalize(data,
                                meta=['areaCode', 'areaName', 'UtlaName'])
        return df
