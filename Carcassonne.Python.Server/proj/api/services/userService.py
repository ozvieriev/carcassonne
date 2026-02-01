from ..repositories.userRepository import userRepository


class userService:
    def __init__(self, repository: userRepository):
        self.repository = repository

    get = lambda self, id: self.repository.get(id)
