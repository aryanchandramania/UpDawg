
from Message.Message import Message
import pymysql
from datetime import datetime,timezone


# maybe make all fetchall returns a dictionary instead of a tuple
# decreases coupling
class MessageDAO:
    def __init__(self, username=None, password=None):
        self.connection = pymysql.connect(
            host="localhost",
            user='raghavd',
            password='password',
            database="messaging"
        )
        self.cursor = self.connection.cursor()

    def add_message(self, message: Message):
        sql = "INSERT INTO messages (MessageID, UserID, Sender, MessageContent, App, Date) VALUES (%s, %s, %s, %s, %s, %s)"
        # values = (MessageID, UserID, Sender, MessageContent, App, Date)
        values = (message.id, message.user_id, message.sender, message.message_content, message.app, message.date)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Message added successfully.")
        except pymysql.Error as error:
            print("Failed to add message:", error)

    # messages is a list of Messages      
    def add_many_messages(self, messages):

        msgs =[]
        for msg in messages: # maybe convert msg into a message object for uniformity ?
            # msgs.append((msg['id'],msg['userId'],msg['sender'],msg['content'],msg['app'],msg['date']))
            # msg.date = datetime.strptime(msg.date, "%Y-%m-%d %H:%M:%S")
            count=0
            if isinstance(msg.id,str):
                count+=1
            if isinstance(msg.user_id,str):
                count+=1
            if isinstance(msg.sender,str):
                count+=1
            if isinstance(msg.message_content,str):
                count+=1
            if isinstance(msg.app,str):
                count+=1
            if isinstance(msg.date,str):
                count+=1
            print(count)
            msgs.append((msg.id, msg.user_id, msg.sender, msg.message_content, msg.app, msg.date))

        # print(msgs)
        sql = "INSERT INTO messages (MessageID, UserID, Sender, MessageContent, App, Date) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.executemany(sql, msgs)
            self.connection.commit()
            print("Messages added successfully.")
        except pymysql.Error as error:
            print("Failed to add messages:", error)
            
    def get_latest_entry(self, app):
        sql = "SELECT * FROM messages WHERE App = %s ORDER BY Date DESC LIMIT 1"
        values = (app,)
        # print(values)
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchone()
            # print(type(result))
            
            res = Message(result[0], result[1], result[2], result[3], result[4], result[5].strftime('%Y-%m-%d %H:%M:%S'))
            # print(res)
            return res
        except Exception as e:
            print("Failed to get latest entry:", e)
            return None
        # except pymysql.Error as error:
        #     print("Failed to get latest entry:", error)
        #     return None 
        # finally:
        #     return None
        
    def get_all_entries(self, app):
        sql = "SELECT * FROM messages WHERE App = %s"
        values = (app)
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            res =[]
            for row in result:
                # indexes????
                res.append(Message(row[0], row[1], row[2], row[3], row[4], row[5].strftime('%Y-%m-%d %H:%M:%S')))
            return res
        except Exception as error:
            print("Failed to get all entries:", error)
            return None

    def get_based_on_date(self,startDate,endDate=None):
        # if endDate is None, return all messages after startDate
        try:
            if endDate is None:
                query = '''SELECT MessageID, UserID, Sender, MessageContent, App, Date
                        FROM messages
                        WHERE Date >= %s'''
                self.cursor.execute(query, (startDate,))
            else:
                query = '''SELECT MessageID, UserID, Sender, MessageContent, App, Date
                        FROM messages
                        WHERE Date BETWEEN %s AND %s'''
                self.cursor.execute(query, (startDate, endDate))
        except pymysql.Error as error:
            print("Failed to get messages:", error)
            return None
        
        data = self.cursor.fetchall()
        res = []
        for row in data:
            res.append(Message(row[0], row[1], row[2], row[3], row[4], row[5].strftime('%Y-%m-%d %H:%M:%S')))
        return res


    def close_connection(self):
        self.connection.close()

# if __name__ == "__main__":
#     # username = input("Enter your MySQL username: ")
#     # password = input("Enter your MySQL password: ")
#     dao = MessageDAO()
#     dao.add_message("!I=s|`,NRc+KZRGv/$7g", "user1", "slackbot", "Hello from Slack!", "Slack", "2021-09-01 12:00:00")
#     dao.add_many_messages([
#         ("aryan`,NRc+KZRGv/$7g", "user1", "slackbot", "Hello from Slack!", "Slack", "2021-09-01 12:00:00"),
#         ("nayra`,NRc+KZRGv/$7g", "user1", "slackbot", "Hello from Slack!", "Slack", "2021-09-01 12:00:00")
#     ])
#     print(dao.get_all_entries("Slack"))
#     dao.close_connection()