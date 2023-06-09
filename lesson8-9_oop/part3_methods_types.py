"""
__new__() overriding: Singleton pattern example
"""


class Singleton:
    """
    The Singleton pattern prohibits the creation of MORE THATN ONE Instance of the specified Class
    When you try to create one more Instance of the Singleton Class, the Reference to the existing Instance
    is returned!
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


# As you can see bellow, 3 Instances of the Singleton class have he SAME Memory Address,
# which means that these Instances are the SAME
s1, s2, s3 = Singleton(), Singleton(), Singleton()
assert s1 is s2 and s1 is s3 and s2 is s3

"""
Methods types: classmethod, staticmethod, property
"""


class MyNewClass:
    NAME = None

    @property
    def name(self):
        """
        property:
        - Provides a possibility to define method as attribute
        - When You will get the 'name' attribute from MyClass Instance
        - после создания Экземпляра Класса и обращении к его АТРИБУТУ
        с именем name - будет вызвван property-метод с именем name
        """
        return f"My name is {self.NAME}"

    @classmethod
    def set_name(cls, name: str):
        """
        classmethod:
        - принимает первым аргументом cls - это ссылка на текущий КЛАСС (не Объект!)
        - внутри classmethod мы можем производить манипуляции с данными, относящимися ко КЛАССУ,
          но НЕ можем манипулировать данными Экземпляра этого Класса
        """
        cls.NAME = name  # здесь NAME - атрибут Класса

    @staticmethod
    def print_hello():
        """
        staticmethod:
        Расположен в КЛАССЕ, но:
        - не обращается к данным КЛАССА
        - не обращается к данным Экземпляра КЛАССА

        Поэтому, вызвать staticmethod можно как от имени Класса, так и от имени его Экземпляра
        """
        print("Hello")

    def print_name(self):
        print(self.NAME)


# Call of 'classmethod' from the Class reference
MyNewClass.set_name("Alex")
# NOTE: You CANNOT call the 'classmethod' from the Instance!

my_class_instance = MyNewClass()
MyNewClass.print_hello()            # Call of 'static' method from the Class reference
my_class_instance.print_hello()     # Call of 'static' method from the Instance reference

# Access to the attribute which marked as 'property'
# leads to the Call of 'property' method
print(my_class_instance.name)


