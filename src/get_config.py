"""load and parse configuration"""
import yaml

# Load YAML config
def load_config(config_path):
# Open the 'config.yaml' file in read mode
    with open(config_path, "r") as stream: # "r" denotes read mode
        try:
            # Load and parse the YAML file safely
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:  # Handle and print any YAML-related errors
            print(exc)