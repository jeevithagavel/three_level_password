# Import main classes and functions to make them easily accessible
from .user_management import add_user, user_exists, send_otp_email, verify_otp, check_password, get_user_email
from .authentication import level_one, level_two, level_three

# You can also define __all__ to control what gets imported with "from package import *"
__all__ = ['add_user', 'user_exists', 'send_otp_email', 'verify_otp', 'check_password', 'get_user_email',
           'level_one', 'level_two', 'level_three']

# Package metadata
__version__ = '1.0.0'
__author__ = 'Your Name'
__license__ = 'MIT'

# You can also include any initialization code here if needed
# For example:
# import logging
# logging.getLogger(__name__).addHandler(logging.NullHandler())
