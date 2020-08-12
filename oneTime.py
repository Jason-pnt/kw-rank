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
flags = True
while flags:
    time_now = time.strftime("%H:%M:%S", time.localtime())
    dates = time.strftime("%Y-%m-%d", time.localtime())
    # pdt_times = datetime.datetime.now(pdt_timezone).strftime("%Y-%m-%d %H:%M:%S")
    if time_now == "07:00:30":
        print(time_now)
        time.sleep(1)
    for i in (os.listdir(os.path.join(father_path, 'keyword'))):
        if i.endswith('csv'):
            print(i + '\n')
            commitName = (i.split('.')[0])
            commitName = commitName + ' CN: ' + dates
            copyfile(os.path.join(father_path, 'keyword', i), os.path.join(father_path, 'test.csv'))
            repo.index.add(['test.csv'])
            repo.index.commit(commitName)
            subprocess.check_call(['git', 'push', 'origin', 'master'])
            time.sleep(10)
    flags = False