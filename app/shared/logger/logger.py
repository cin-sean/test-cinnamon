import yaml
import logging.config

# Pull in Logging Config
with open('logger-config.yaml', 'r') as stream:
  try:
    logging_config = yaml.load(stream, Loader=yaml.SafeLoader)
    logging.config.dictConfig(logging_config)
  except yaml.YAMLError as exc:
    print("Error Loading Logger Config")
    pass
