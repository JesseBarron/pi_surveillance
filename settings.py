# Import the config file. And set app.config
import config
import sys
app = {}

if __name__ == "main":
  env = sys.argv[1] if len(sys.argv) > 2 else 'dev'
  
  if env == 'dev':
    app['config'] = config.DevConfig
  elif env == 'test':
    app.config = config.TestConfig
  elif env == 'prod':
    app.config = config.ProductionConfig
  else:
    raise ValueError("Invalid env variable given")
