import time

from part_1.homework.task_1 import Auto


class Car(Auto):

    def __init__(self, brand: str, age: int, mark: str, max_speed: int, color: str = "red", weight: int = 2000):
        super().__init__(brand, age, mark, color=color, weight=weight)
        self.max_speed = max_speed

    def move(self):
        super(Car, self).move()
        print(f"Max speed is {self.max_speed}")


class Truck(Auto):

    def __init__(self, brand: str, age: int, mark: str, max_load: int, color: str = "white", weight: int = 10_000):
        super().__init__(brand, age, mark, color=color, weight=weight)
        self.max_load = max_load

    def move(self):
        print("Attention!")
        super(Truck, self).move()

    @staticmethod
    def load():
        time.sleep(1)
        print("Load ...")
        time.sleep(1)


# TEST
car1 = Car("Mercedes", 10, "C 230", 250, weight=2_500)
car2 = Car("Tesla", 2, "Model S", 300, color="green")

truck1 = Truck("MAZ", 20, "", 250, weight=25_000)
truck2 = Truck("KAMAZ", 15, "", 300, color="gray", weight=20_000)

for instance in (car1, car2, truck1, truck2):
    print(f"Instance: {instance}")

    for name, value in instance:
        print(f"Attribute '{name}' has value: {value}")

    instance.move()

    if isinstance(instance, Truck):
        instance.load()

    print("-" * 30)
