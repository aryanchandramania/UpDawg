import json
import hashlib
from cryptography.fernet import Fernet
import os    
from filelock import Timeout, FileLock

class UserManager:
    def __init__(self):
        self.user_data = []
        self.bestSer_path = "LLMService.json"
        self.lock_path = "LLMService.txt.lock"
        self.lock = FileLock(self.lock_path, timeout=2)

        try:
            with open("user_data.json", "r") as file:
                self.user_data = json.load(file)
        except:
            pass

    def generate_key(self):
        return Fernet.generate_key()

    def encrypt(self, data, key):
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt(self, encrypted_data, key):
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def store_user_data(self, username, email, password, gemini_api_key, openai_api_key, slack_email, slack_id):
        # Generate keys for API key encryption
        gemini_key = self.generate_key()
        openai_key = self.generate_key()

        # Encrypt API keys
        encrypted_ga_key = self.encrypt(gemini_api_key, gemini_key)
        encrypted_oa_key = self.encrypt(openai_api_key, openai_key)

        # Hash password
        hashed_password = self.hash_password(password)

        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "gemini_api_key": encrypted_ga_key.decode(),
            "gemini_api_key_key": gemini_key.decode(),
            "openai_api_key": encrypted_oa_key.decode(),
            "openai_api_key_key": openai_key.decode(),
            "slack_email": slack_email,
            "slack_id": slack_id,
            "is_login": False
        }

        for user in self.user_data:
            if user["username"] == user_data["username"]:
                print("User already exists in database")
                return
            
        self.user_data.append(user_data)

        # Store user data in JSON file
        with open("user_data.json", "w") as file:
            json.dump(self.user_data, file)


    def load_user_data(self):
        with open("user_data.json", "r") as file:
            self.user_data = json.load(file)

        loaded_users = []
        for user in self.user_data:
            # Decrypt API keys
            gemini_api_key = self.decrypt(user["gemini_api_key"], user["gemini_api_key_key"])
            openai_api_key = self.decrypt(user["openai_api_key"], user["openai_api_key_key"])

            loaded_users.append({
                "username": user["username"],
                "email": user["email"],
                "password": user["password"],
                "gemini_api_key": gemini_api_key,
                "openai_api_key": openai_api_key,
                "slack_email": user["slack_email"],
                "slack_id": user["slack_id"],
                "is_login": user["is_login"]
            })

        return self.user_data, loaded_users
    
    def get_keys(self):
        keys = {
            "gemini": None,
            "openai": None
        }
        self.user_data, users = self.load_user_data()
        for user in users:
            if user["is_login"] == True:
                keys["gemini"] = user["gemini_api_key"]
                keys["openai"] = user["openai_api_key"]
                return keys
        return keys
    


    def login(self, username, password):
        self.user_data, _ = self.load_user_data()
        for i,user in enumerate(self.user_data):
            if user["username"] == username:
                stored_password = user["password"]
                # Hash entered password
                entered_password_hash = self.hash_password(password)
                # Compare hashed passwords
                if stored_password == entered_password_hash:
                    print("Login successful!")
                    user["is_login"] = True
                    with open("user_data.json", "w") as file:
                        json.dump(self.user_data, file)
                    # Update the json file
                    return True
                else:
                    print("Incorrect password!")
                    return False
        print("User not found!")
        return False

    def logout(self):
        self.user_data, _ = self.load_user_data()
        for user in self.user_data:
            if user["is_login"] == True:
                user["is_login"] = False
                with open("user_data.json", "w") as file:
                    json.dump(self.user_data, file)
                print(f"{user['username']} logged out successfully.")
                return True
        print("No one is logged in")
        return False
    
    def setBestService(self, ser):
        data = {'bestService': ser}
        try:
            with self.lock.acquire(timeout=2):
                with open(self.bestSer_path, "w") as f:
                    json.dump(data, f)
                    print("Best service set successfully.")
        except Timeout:
            print("Another instance of this application currently holds the lock.")

    def getBestService(self):
        try:
            with self.lock.acquire(timeout=2):
                with open(self.bestSer_path, "r") as f:
                    data = json.load(f)
                    return data.get('bestService', None)
        except Timeout:
            print("Another instance of this application currently holds the lock.")
        return None


if __name__ == "__main__":
    # Example usage
    user_manager = UserManager()

    # Storing user data
    user_manager.store_user_data(
        username="JohnDoe",
        email="john@example.com",
        password="password123",
        gemini_api_key="gemini_api_key_value",
        openai_api_key="openai_api_key_value",
        slack_email="john@slack.com",
        slack_id="U12345678"
    )

    user_manager.store_user_data(
        username="JaneDoe",
        email="jane@example.com",
        password="janespassword",
        gemini_api_key="another_gemini_api_key_value",
        openai_api_key="another_openai_api_key_value",
        slack_email="jane@slack.com",
        slack_id="U87654321"
    )

    # Logging in
    user_manager.login("JohnDoe", "password123")
    print(user_manager.get_keys())

    # Logging out
    user_manager.logout()
    user_manager.login("JaneDoe", "janespassword")
    print(user_manager.get_keys())

    user_manager.setBestService("gemini")
    print(user_manager.getBestService())
