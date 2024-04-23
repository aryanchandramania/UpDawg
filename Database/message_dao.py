import sys
sys.path.append('..')
from Message.Message import Message
import pymysql


# maybe make all fetchall returns a dictionary instead of a tuple
# decreases coupling
class MessageDAO:
    def __init__(self, username, password):
        self.connection = pymysql.connect(
            host="localhost",
            user=username,
            password=password,
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
            msgs.append((msg.id, msg.user_id, msg.sender, msg.message_content, msg.app, msg.date))

        sql = "INSERT INTO messages (MessageID, UserID, Sender, MessageContent, App, Date) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.executemany(sql, messages)
            self.connection.commit()
            print("Messages added successfully.")
        except pymysql.Error as error:
            print("Failed to add messages:", error)
            
    def get_latest_entry(self, app):
        sql = "SELECT * FROM messages WHERE App = %s ORDER BY Date DESC LIMIT 1"
        values = (app)
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchone()

            # indexes???
            res = Message(result[1], result[2], result[3], result[4], result[5], result[6])
            return res
        except pymysql.Error as error:
            print("Failed to get latest entry:", error)
            return None 
        
    def get_all_entries(self, app):
        sql = "SELECT * FROM messages WHERE App = %s"
        values = (app)
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            res =[]
            for row in result:
                # indexes????
                res.append(Message(row[1], row[2], row[3], row[4], row[5], row[6]))
            return res
        except pymysql.Error as error:
            print("Failed to get all entries:", error)
            return None

    def get_based_on_date(self,startDate,endDate=None):
        # if endDate is None, return all messages after startDate
        try:
            if endDate is None:
                query = '''SELECT App, MessageID, UserID, Sender, MessageContent, Date
                        FROM messages
                        WHERE Date >= ?'''
                self.cursor.execute(query, (startDate,))
            else:
                query = '''SELECT App, MessageID, UserID, Sender, MessageContent, Date
                        FROM messages
                        WHERE Date BETWEEN ? AND ?'''
                self.cursor.execute(query, (startDate, endDate))
        except pymysql.Error as error:
            print("Failed to get messages:", error)
            return None
        
        data = self.cursor.fetchall()
        res = []
        for row in data:
            res.append(Message(row[1], row[2], row[3], row[4], row[5], row[6]))
        return res


    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    username = input("Enter your MySQL username: ")
    password = input("Enter your MySQL password: ")
    dao = MessageDAO(username, password)
    dao.add_message("!I=s|`,NRc+KZRGv/$7g", "user1", "slackbot", "Hello from Slack!", "Slack", "2021-09-01 12:00:00")
    dao.add_many_messages([
        ("aryan`,NRc+KZRGv/$7g", "user1", "slackbot", "Hello from Slack!", "Slack", "2021-09-01 12:00:00"),
        ("nayra`,NRc+KZRGv/$7g", "user1", "slackbot", "Hello from Slack!", "Slack", "2021-09-01 12:00:00")
    ])
    print(dao.get_all_entries("Slack"))
    dao.close_connection()