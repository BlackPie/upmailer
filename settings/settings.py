# Proxy mail settings
IMAP_HOST = 'imap.gmail.com'

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

PROXY_EMAIL = None
PROXY_PASSWORD = None

# Mail settings
DESTINATION_EMAIL = None
DESTINATION_PASSWORD = None

# Fetching settings
MAX_NUMBER_OLD_MESSAGES = 10
LANCEMONITOR_EMAIL = 'mailer@lancemonitor.com'


# Filtering settings
# Options: LESS_THAN_10HOURS, BETWEEN_1030HOURS, MORE_THAN_30HOURS
NEEDED_WORKLOAD = None

# Minimal reward for fixed jobs
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

try:
    from local_settings import *
except ImportError:
    pass
