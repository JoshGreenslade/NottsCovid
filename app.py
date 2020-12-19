import json
import dash

# Load in configuration
with open('./config/nottsConfig.json', 'r') as f:
    config = json.load(f)

# Init the app
app = dash.Dash(__name__)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=config['debug'])
