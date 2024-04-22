import mysql.connector

def create_database(username, password):
    connection = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password
    )

    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS messaging")
    cursor.execute("USE messaging")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            MessageID VARCHAR(255),
            UserID VARCHAR(255),
            Sender VARCHAR(255),
            MessageContent TEXT,
            App VARCHAR(50),
            PRIMARY KEY (MessageID, App)
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    username = input("Enter your MySQL username: ")
    password = input("Enter your MySQL password: ")
    create_database(username, password)