import logging.config

import yaml

# Pull in Logging Config
with open("logger-config.yaml") as stream:
    try:
        logging_config = yaml.load(stream, Loader=yaml.SafeLoader)
        logging.config.dictConfig(logging_config)
    except yaml.YAMLError:
        print("Error Loading Logger Config")
