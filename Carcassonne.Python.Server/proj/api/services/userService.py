from ..repositories.userRepository import userRepository


class userService:
    def __init__(self, repository: userRepository):
        self.repository = repository

    def get(self, id): return self.repository.get(id)
