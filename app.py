import json
import dash
from src import dataCtrl

# Load in configuration
with open('./config/nottsConfig.json', 'r') as f:
    config = json.load(f)

data_ctrl = dataCtrl.DataCtrl()
print(data_ctrl.get_data_for_area('E02006905'))

# Init the app
app = dash.Dash(__name__)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=config['debug'])
