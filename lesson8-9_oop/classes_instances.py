
"""
This is Class - a layer of Abstraction, which provides a possibility to create our owm types!
('Class' and 'Type' are synonyms in Python)
"""

class MyClass:

    """
    This is Class attributes: it's visible to all code within the current Class
    """
    URL = "https://google.com"
    some = "SOME"

    def __init__(self, url: str):
        """
        This is Instance (in terms 'Instance of the Class') attributes.
        It's visible to all Methods in Class which takes 'self' as first argument
        """
        self.url = url
        self.some = "some"  # this is not the same 'some' that is declared on Class level!

    def some_method(self):
        """
        This is method: as standard function but which is bound to the Instance of this Class
        """
        print(self.url)  # print 'some' value which is declared in __init__: Instance attribute
        print(self.URL)  # but via 'self' we can have access to the Class attributes too


my_class = MyClass  # reference to the MyClass object
print(type(my_class))  # Class object has type 'type' :)
my_instance = MyClass(url="https://amazon.com")  # my_instance is the Instance of the class MyClass
print(type(my_instance))  # Instance has type by the name of its Class

# Attributes access
print(my_class.URL)  # read the class attribute
print(my_class.some)  # read the class attribute

print(my_instance.url)  # read the instance attribute
print(my_instance.some)  # read the instance attribute

my_class.some = "another some Class value"
my_instance.some = "another some Instance value"  # update the Instance existing attribute value
print(my_class.some)
print(my_instance.some)

del my_instance.some     # deleting of attribute is also possible!
print(my_instance.some)  # will print the Class 'some' because the Instance 'some' was deleted!

my_instance.new_attr = "New attribute"  # Also it's possible to set NEW attribute to the Instance
print(my_instance.new_attr)
