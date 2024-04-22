import sys
sys.path.append('..')
from Database import message_dao

class DataEngine:
    def __init__(self):

    def pushData(self):

    def checkGap(self):
        

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