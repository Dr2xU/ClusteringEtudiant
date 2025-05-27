class User: 
    def __init__(self, user_id, email, password, role):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f"User(user_id={self.user_id}, email='{self.email}')"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email
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
    