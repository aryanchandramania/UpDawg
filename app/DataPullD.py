# this is the driver code for data pull
# it calls the pullData function from the DataPull.py file periodically

# from src.DataPull.Outlook import OutlookDataPull
# from src.DataPull.Slack import SlackDataPull

from time import sleep
import asyncio

import sys
sys.path.append("../src")

from DataClasses.MessageServices import MessageServices
from DataEngine.DataEngine import DataEngine

period = 120 # in seconds
de = DataEngine()
msgSerData = MessageServices()

app_names = msgSerData.service_names
apps = msgSerData.getServices()

async def main():
    while True:
        latest_entries = de.checkGap()
        # print(latest_entries)
        for app_name in app_names:
            if latest_entries[app_name] is not None:
                if app_name == 'Slack':
                    gapData = apps[app_name].pullData(latest_entries[app_name])
                elif app_name == 'Outlook':
                    gapData = await apps[app_name].pullData(latest_entries[app_name])
                de.pushData(gapData)
        sleep(period)

if __name__ == "__main__":
    asyncio.run(main())