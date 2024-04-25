

class Message:
    def __init__(self, id = None, user_id = None, sender = None, message_content= None, app = None, date = None):
        self.user_id = user_id
        self.sender = sender
        self.message_content = message_content
        self.date = date
        self.id = id
        self.app = app

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sender': self.sender,
            'message_content': self.message_content,
            'date': self.date,
            'app': self.app
        }

    def from_dict(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.sender = data['sender']
        self.message_content = data['message_content']
        self.date = data['date']
        self.app = data['app']


    def __str__(self):
        return f"Message: {self.id}, {self.user_id}, {self.sender}, {self.message_content}, {self.date}, {self.app}"