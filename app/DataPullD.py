# this is the driver code for data pull
# it calls the pullData function from the DataPull.py file periodically

# from src.DataPull.Outlook import OutlookDataPull
# from src.DataPull.Slack import SlackDataPull

from time import sleep

import sys
sys.path.append('/home/shashwat/Desktop/IIITH/Year3_Sem2/SE/Project3/UpDawg/src/')

from DataClasses.MessageServices import MessageServices
from DataEngine.DataEngine import DataEngine

period = 120 # in seconds
de = DataEngine()
msgSerData = MessageServices()

app_names = msgSerData.service_names
apps = msgSerData.getServices()


while True:
    latest_entries = de.checkGap()
    for app_name in app_names:
        if latest_entries[app_name] is not None:
            gapData = apps[app_name].pullData(latest_entries[app_name])
            de.pushData(gapData)
    sleep(period)