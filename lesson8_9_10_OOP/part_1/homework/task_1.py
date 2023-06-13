class Auto:

    def __init__(self, brand: str, age: int, mark: str, color: str = "black", weight: int = 1000):
        self.brand = brand
        self.age = age
        self.mark = mark
        self.color = color
        self.weight = weight

    def __iter__(self):
        for attr_name, attr_value in self.__dict__.items():
            yield attr_name, attr_value

    @staticmethod
    def move():
        print("Move!")

    @staticmethod
    def stop():
        print("Stop!")

    def birthday(self):
        self.age += 1

