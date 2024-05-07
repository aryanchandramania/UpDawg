
from Database import message_dao
# from DataPull.Outlook import OutlookDataPull
# from DataPull.Slack import SlackDataPull
from DataClasses.MessageServices import MessageServices
from Message.Message import Message
import asyncio

import datetime
from datetime import timezone 
import pytz


# check if all times are in UTC
class DataEngine:
    def __init__(self):
        self.msg_dao = message_dao.MessageDAO()
        msgSerData = MessageServices()
        self.app_names = msgSerData.service_names
        self.apps = msgSerData.getServices()
        # self.app_names = ['Slack', 'Outlook']
        # self.apps = {
        #     'Slack': SlackDataPull(), # check if this instantiation is correct
        #     'Outlook': OutlookDataPull()
        # }
        self.tolerance = datetime.timedelta(minutes=1)


    # messages is a list of Messages
    def pushData(self, messages):
        self.msg_dao.add_many_messages(messages)
        

    # check if datetimes are correct here
    # should return a datetim object in the dictionary
    def checkGap(self, initStartdate = None):
        cur_time = datetime.datetime.now(timezone.utc)
        latest_times = {}
        for app in self.app_names:
            latest_times[app] = None
            latest_entry = self.msg_dao.get_latest_entry(app)
            if latest_entry is None:
                print(f"No entry found for {app}")
                latest_times[app] = initStartdate
                continue
            latest_times[app] = pytz.utc.localize(datetime.datetime.strptime(latest_entry.date, "%Y-%m-%d %H:%M:%S"))
            if cur_time - latest_times[app] < self.tolerance:
                latest_times[app] = None
        return latest_times
        

    # returns a dictionary of messages grouped by App
    # {AppName:[Message, ...], ...}    
    def getDataFromDB(self, startDate):
        data = self.msg_dao.get_based_on_date(startDate.strftime("%Y-%m-%d %H:%M:%S"))

        if data is None:
            return None

        # group by App and return data in the form of a dictionary
        result = {}
        for row in data:
            app = row.app

            if app not in result:
                result[app] = []
            
            result[app].append(row)
        print(result.keys())
        return result
    
    
    # public facing function
    async def getData_async(self,startDate):
        latest_entries = self.checkGap(startDate)
        for app_name in self.app_names:
            if latest_entries[app_name] is not None:
                if app_name == 'Slack':
                    gapData = self.apps[app_name].pullData(latest_entries[app_name])
                    # print(gapData)
                elif app_name == 'Outlook':
                    gapData = await self.apps[app_name].pullData(latest_entries[app_name])
                self.pushData(gapData)
                print(f"Data for {app_name} pulled and pushed to DB")
        print("Data pulled and pushed to DB")
        return self.getDataFromDB(startDate)
    
    def getData(self,startDate):
        return asyncio.run(self.getData_async(startDate))
    

        