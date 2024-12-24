from pathlib import Path
import yaml
from typing import Dict, Any

def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate required fields
        required_fields = ['repo_path', 'watch_path']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")
        
        # Convert paths to absolute paths
        config['repo_path'] = str(Path(config['repo_path']).resolve())
        config['watch_path'] = str(Path(config['watch_path']).resolve())
        
        return config
        
    except Exception as e:
        raise Exception(f"Failed to load config: {str(e)}") 