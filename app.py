import json
import dash
import dataCtrl

# Load in configuration
with open('./config/nottsConfig.json', 'r') as f:
    config = json.load(f)

# Init the app
app = dash.Dash(__name__)
data_ctrl = dataCtrl.DataCtrl()
server = app.server

# Run the app
if __name__ == '__main__':
    app.run_server(debug=config['debug'])
