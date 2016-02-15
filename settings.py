from constants import *


# Email settings
IMAP_HOST = 'imap.gmail.com'
EMAIL = 'avaneratestemail@gmail.com'
PASSWORD = 'avaneratest'


# Fetching settings
MAX_NUMBER_OLD_MESSAGES = 10
# LANCEMONITOR_EMAIL = 'mailer@lancemonitor.com'
LANCEMONITOR_EMAIL = 'fedotkin.dmitry@gmail.com'


# Filtering settings
# Options: LESS_THAN_10HOURS, BETWEEN_1030HOURS, MORE_THAN_30HOURS
NEEDED_WORKLOAD = None

# Just type minimal number no matter hourly or fixed you mean
NEEDED_BUDGET = None

# Duration of a project. Options: LESS_THAN_1MONTH, BETWEEN_13_MONTHS, MORE_THAN_6MONTHS
NEEDED_DURATION = None

# Options: HOURLY, FIXED
NEEDED_JOB_TYPE = None

# Client minimal posted jobs amount
NEEDED_JOB_POSTED_MIN = None

# Client minimal hires amount
NEEDED_HIRES_MIN = None

# Client hire ratio in percents
NEEDED_HIRE_RATIO = None

# Clinet rating. Number from 0 to 5 woth 0.1 precise
NEEDED_RATING_MIN = None

# Client minimal reviews amount
NEEDED_REVIEWS_MIN = None
