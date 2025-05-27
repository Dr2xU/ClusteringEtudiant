class user: 
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}')"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password
        }
    
    def login(self):
        """
        Connection to the user account.
        """
        pass

    def logout(self):
        """
        Disconnect from the user account.
        """
        pass