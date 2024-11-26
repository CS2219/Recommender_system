import yaml

# Function to load API keys from config.yaml
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)
