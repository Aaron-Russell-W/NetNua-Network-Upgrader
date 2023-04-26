import os
import time
import schedule
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetNua.settings')
import django
django.setup()
from upgrades.views import check_upgrades

def run_check_upgrades():
    check_upgrades(None)


schedule.every(5).minutes.do(run_check_upgrades)

while True:
    schedule.run_pending()
    time.sleep(1)
