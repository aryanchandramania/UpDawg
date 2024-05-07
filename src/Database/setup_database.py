import pymysql

def create_database(username = None, password = None):
    connection = pymysql.connect(
        host="localhost",
        user='root',
        password="aryan"
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
            Date DATETIME,
            PRIMARY KEY (MessageID, App)
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    # username = input("Enter your MySQL username: ")
    # password = input("Enter your MySQL password: ")
    create_database()