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
        

    # returns a dictionary of messages grouped by App
    # {AppName:[{MessageID, UserID, Sender, MessageContent, Date}, ...], ...}    
    def getDataFromDB(self, startDate):
        data = self.msg_dao.get_based_on_date(startDate.strftime("%Y-%m-%d %H:%M:%S"))

        if data is None:
            return None

        # group by App and return data in the form of a dictionary
        result = {}
        for row in data:
            app = row[0]
            sender = row[3]
            message_content = row[4]
            date = row[5]
            
            if app not in result:
                result[app] = []
            
            result[app].append({
                'App': app,
                'Sender': sender,
                'MessageContent': message_content,
                'Date': date
            })
        
        return result