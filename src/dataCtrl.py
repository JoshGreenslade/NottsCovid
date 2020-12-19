import datetime
import json

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

    def update_data(self):
        """ Updates the local and stored data from the API """

        time_now = datetime.datetime.utcnow()

        config['lastUpdated'] = time_now.strftime(self.time_format)

        with open('./config/nottsConfig.json', 'w') as f:
            json.dump(config, f, indent=4)
