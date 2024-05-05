


from DataPull.Slack.SlackDataPull import SlackDataPull
from DataPull.Outlook.OutlookDataPull import OutlookDataPull

class MessageServices:
    def __init__(self):
        self.service_names = ['Slack', 'Outlook']

    def getServices(self):
        services = {
            'Slack': SlackDataPull(), # check if this instantiation is correct
            'Outlook': OutlookDataPull()
        }
        return services