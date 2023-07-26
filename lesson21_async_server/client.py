class UserClient:

    def __init__(self, name: str, age: int, gender: str, nationality: str = "belarus"):
        self._name = name
        self._age = age
        self._gender = gender
        self._nationality = nationality

    async def add_post(self):
        pass

    async def add_comment(self, post_title: str):
        pass

    async def add_like(self, post_title: str):
        pass

    async def edit_post(self, post_title: str, edit_data: dict[str, str]):
        pass

    async def edit_comment(self, comment_title: str):
        pass

    def delete_post(self, post_title: str):
        pass

    def delete_comment(self, comment_title: str):
        pass

    def delete_like(self, post_title: str):
        pass