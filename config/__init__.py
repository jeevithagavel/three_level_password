# Import the db_config to make it easily accessible
from .db_config import db_config

# Define __all__ to control what gets imported with "from config import *"
__all__ = ['db_config']

# You can add package metadata if needed
__version__ = '1.0.0'
__author__ = 'Your Name'

# If you have any initialization code for your config, you can add it here
# For example:
# import logging
# logging.getLogger(__name__).addHandler(logging.NullHandler())

# You can also add any configuration loading logic here if needed
# For example:
# def load_config():
#     # Load configuration from a file or environment variables
#     pass
# 
# load_config()
