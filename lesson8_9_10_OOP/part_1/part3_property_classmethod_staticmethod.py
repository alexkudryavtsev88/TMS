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
        - takes 'cls' as first argument (reference to the Class in which the method is defined)
        - inside the 'classmethod' we have access to data related to the Class, not Instance!
        """
        cls.NAME = name

    @staticmethod
    def print_hello():
        """
        staticmethod:

        when we:
        - no need to have Class reference (cls) in the method
        - no need to have Instance reference (self) in the method

        We marked the method as 'staticmethod'
        and we can call the 'staticmethod' both from the Class and from the Instance
        """
        print("Hello")

    def print_name(self):
        print(self.NAME)


my_class_instance = MyNewClass()

# Access to the attribute which marked as 'property'
# leads to the Call of 'property' method
my_name = my_class_instance.name
print(my_name)  # will print "My name is None"

# Call of 'classmethod' from the Class reference
MyNewClass.set_name("Alex")
# NOTE: You CANNOT call the 'classmethod' from the Instance!
print(my_class_instance.name)  # will print "My name is Alex"

MyNewClass.NAME = "TEST"
print(my_class_instance.name)  # will print "My name is Alex"

MyNewClass.print_hello()            # Call of 'static' method from the Class reference
my_class_instance.print_hello()     # Call of 'static' method from the Instance reference



