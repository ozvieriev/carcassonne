class userModel():
    __tablename__ = "users"

    def __init__(self, id, email):
        self.id = id
        self.email = email