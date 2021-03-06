import datetime
import json
import requests
import pandas as pd
from pandas import json_normalize
import ast

# Load in configuration
with open('./config/nottsConfig.json', 'r') as f:
    config = json.load(f)


class DataCtrl:
    """ A class for controlling the data and API interaction """

    def __init__(self):

        self.time_format = "%Y-%m-%d %H:%M:%S"

        self.endpoint = 'https://coronavirus.data.gov.uk/api/v1/soa?'

        # Update the data if needed.
        last_updated = datetime.datetime.strptime(
            config['lastUpdated'], self.time_format)
        time_now = datetime.datetime.utcnow()
        if (time_now - last_updated > datetime.timedelta(days=1)):
            self.update_data()

        # Get the data
        self.data = pd.read_csv('./data/nottsData.csv')

        # Get the data as a time-series
        df = self.data
        df['newCasesBySpecimenDate'] = df['newCasesBySpecimenDate'].apply(
            ast.literal_eval)
        df_list = []
        for idx, row in df.iterrows():
            i = pd.DataFrame(row['newCasesBySpecimenDate'])
            i['areaName'] = row['areaName']
            i['areaCode'] = row['areaCode']
            i['UtlaCode'] = row['UtlaCode']
            i['UtlaName'] = row['UtlaName']
            i['LtlaCode'] = row['LtlaCode']
            i['LtlaName'] = row['LtlaName']
            i['date'] = pd.to_datetime(i['date'])
            df_list.append(i)
        self.time_series = pd.concat(df_list)

        # Init the geojson
        with open(config['geojsonPath']) as geofile:
            geojson = json.load(geofile)
            # These next lines ensure the geography shows up on maps
            # Something to do with dash expecting an ID column.
            for feature in geojson["features"]:
                feature['id'] = feature['properties']['msoa11cd']
        self.geojson = geojson

    def update_data(self):
        """ Updates the local and stored data from the API """

        # Get the new data
        data = self.get_data_for_all_areas()
        data.to_csv('./data/nottsData.csv')

        # Update the config file
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
        """Query the API for the msoa details on a given area code

        :param area_code: The area code to query
        :type area_code: str
        :return: A pandas DataFrame
        :rtype: pd.DataFrame
        """

        filter = f'filters=&areaType=msoa&areaCode={area_code}'
        data = self.get(filter=filter)
        if data is not None:
            df = json_normalize(data,
                                meta=['areaCode', 'areaName', 'UtlaName'])
        else:
            return None
        return df

    def get_data_for_all_areas(self):
        """Query the API for all area codes. Return a dataframe.

        :return: A pandas dataframe containing all the API information
        :rtype: pd.DataFrame
        """

        df_list = []
        for area_code in config['areaCodes']:
            print(area_code)
            df_list.append(self.get_data_for_area(area_code))
        df = pd.concat(df_list)
        return df
