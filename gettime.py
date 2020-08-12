import time
import pytz
import datetime

pst_timezone=pytz.timezone("America/Los_Angeles")
time_now = time.strftime("%H:%M:%S", time.localtime())
dates = time.strftime("%Y-%m-%d", time.localtime())
print(datetime.datetime.now(pst_timezone).strftime("%Y-%m-%d %H:%M:%S"))
print(dates, time_now)