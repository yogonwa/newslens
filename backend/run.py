import uvicorn
import yaml
from pathlib import Path

# Load configuration
config_path = Path(__file__).parent / "config" / "development.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=config["api"]["host"],
        port=config["api"]["port"],
        reload=config["api"]["debug"]
    ) 