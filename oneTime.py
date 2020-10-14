from git import Repo
import os
import subprocess
import sys
import time
import datetime
import pytz
from shutil import copyfile
current_path=(os.path.abspath(__file__))
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")

repo = Repo(os.path.abspath(father_path))
pdt_timezone=pytz.timezone("America/Los_Angeles")

time_now = time.strftime("%H:%M:%S", time.localtime())
dates = time.strftime("%Y-%m-%d", time.localtime())

commitName = 'test.csv' + ' CN: ' + dates
repo.index.add(['*'])
repo.index.commit(commitName)
subprocess.check_call(['git', 'push', 'origin', 'master'])            
