# this is the driver code for data pull
# it calls the pullData function from the DataPull.py file periodically

from src.DataPull.Outlook import OutlookDataPull
from src.DataPull.Slack import SlackDataPull
from src.DataEngine.DataEngine import DataEngine
from time import sleep


period = 120 # in seconds
de = DataEngine()


app_names = ['Slack', 'Outlook']
apps = {
    'Slack': SlackDataPull(), # check if this instantiation is correct
    'Outlook': OutlookDataPull()
}


while True:
    latest_entries = de.checkGap()
    for app_name in app_names:
        if latest_entries[app_name] is not None:
            gapData = apps[app_name].pullData(latest_entries[app_name])
            de.pushData(gapData)
    sleep(period)