import sys
sys.path.append('..')
from Database import message_dao

import datetime

class DataEngine:
    def __init__(self):
        self.msg_dao = message_dao.MessageDAO("root", "password")
        self.app_names = ['Slack', 'Outlook']
        self.tolerance = datetime.timedelta(minutes=1)

    def pushData(self):
        

    def checkGap(self):
        cur_time = datetime.datetime.now()
        latest_times = {}
        for app in self.app_names:
            latest_entry = self.msg_dao.get_latest_entry(app)
            latest_times[app] = latest_entry[-1]
            if latest_entry is None:
                print(f"No entry found for {app}")
                continue
            if cur_time - latest_entry[-1] < self.tolerance:
                latest_times[app] = None
        return latest_times
        
    def getDataFromDB(self):