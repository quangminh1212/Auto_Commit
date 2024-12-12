import yaml
import logging

class Config:
    def __init__(self, config_path='config/settings.yaml'):
        self.config_path = config_path
        self.settings = self.load_config()
        
    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logging.error(f"Failed to load config: {str(e)}")
            return {} 