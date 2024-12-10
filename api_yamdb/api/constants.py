from django.conf import settings
from pathlib import Path

CSV_DIR = Path(settings.BASE_DIR) / 'static/data/'
MAX_LENGTH_TITLE = 256
MAX_STR_LENGTH = 15