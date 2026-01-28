from ..models import userModel

class userRepository:
    def __init__(self):
        pass

    def get(self, id: int) -> userModel | None:
        return userModel(id=id, email="example@example.com")