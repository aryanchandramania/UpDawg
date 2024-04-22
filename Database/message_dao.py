import pymysql

class MessageDAO:
    def __init__(self, username, password):
        self.connection = pymysql.connect(
            host="localhost",
            user=username,
            password=password,
            database="messaging"
        )
        self.cursor = self.connection.cursor()

    def add_message(self, MessageID, UserID, Sender, MessageContent, App, Date):
        sql = "INSERT INTO messages (MessageID, UserID, Sender, MessageContent, App, Date) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (MessageID, UserID, Sender, MessageContent, App, Date)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            print("Message added successfully.")
        except pymysql.Error as error:
            print("Failed to add message:", error)

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    username = input("Enter your MySQL username: ")
    password = input("Enter your MySQL password: ")
    dao = MessageDAO(username, password)
    dao.add_message("!I=s|`,NRc+KZRGv/$7g", "user1", "slackbot", "Hello from Slack!", "Slack", "2021-09-01 12:00:00")
    dao.close_connection()