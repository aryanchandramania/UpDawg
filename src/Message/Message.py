

class Message:
    def __init_(self, id, user_id, sender, message_content, app, date, conv_id=None):
        self.user_id = user_id
        self.conversation_id = conv_id # reqd only for Slack; (conv_id, ts) => unique message
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
    
    def __str__(self):
        return f"Message: {self.id}, {self.user_id}, {self.sender}, {self.message_content}, {self.date}, {self.app}"