"""
Class and Instance of the Class
"""

"""
This is Class below - a layer of Abstraction, which provides a possibility to create our owm types!
('Class' and 'Type' are synonyms in Python)
"""


class MyClass:

    """
    This is Class attributes: it's visible to all code within the current Class
    """
    URL = "https://google.com"
    some = "MyClass some"

    def __init__(self, url: str):
        """
        This is Instance (in terms 'Instance of the Class') attributes.
        It's visible to all Methods in Class which takes 'self' as first argument
        """
        self.url = url
        self.some = "MyClass Instance some"  # this is not the same 'some' that is declared on Class level!

    def some_method(self):
        """
        This is method: as standard function but which is bound to the Instance of this Class
        """
        print(self.url)  # print 'some' value which is declared in __init__: Instance attribute
        print(self.URL)  # but via 'self' we can have access to the Class attributes too


class MyClass2(MyClass):
    """
    MyClass2 is INHERITED from MyClass
    """
    some = "MyClass2 some"

    def __init__(self, url: str):
        super().__init__(url)
        self.some = "MyClass2 Instance some"


"""
Creating the Class Instance
"""
my_class = MyClass  # reference to the MyClass object
print(type(my_class))  # Class object has type 'type' :)

# creating Instance of the MyClass (__init__ method is called underlying)
my_instance = MyClass(url="https://amazon.com")
print(type(my_instance))  # Instance has type by the name of its Class

"""
Attributes access
"""

# READ Attribute:
print(my_class.URL)  # read the class attribute
print(my_class.some)  # read the class attribute

print(my_instance.url)  # read the instance attribute
print(my_instance.some)  # read the instance attribute

# UPDATE EXISTING Attribute
my_class.some = "MyClass NEW some"              # update the Class existing attribute value
my_instance.some = "MyClass Instance NEW some"  # update the Instance existing attribute value
print(my_class.some)
print(my_instance.some)

# ADD NEW Attribute:
my_instance.new_attr = "New attribute"
print(my_instance.new_attr)

# DELETE Attribute:
del my_instance.some     # deleting of attribute is also possible!

"""
Attributes Lookup Algorithm
"""

print(my_instance.some)  # will print the Class 'some' because the Instance 'some' was deleted at line 70
# This happens because if Attribute by the specified name was NOT found in Instance,
# the Attributes Lookup Algorithm will search for attributes with this name in Instance's Class!

# NOTE: This is not good practice to set Class attribute and Instance attribute with the SAME name!

# Instance's Methods
my_instance.some_method()  # call of method belongs to the Instance (cannot call it from the Class!)
# 'self' (first argument of the method) should NOT be specified explicitly when we call the method!
# It's needed just for identifying that the method is bound to the Instance of the Class

""" 
Instances and Classes in Memory
"""

x = MyClass(url="test")
y = MyClass(url="test")
z = MyClass(url="test")
assert id(x) != id(y) != id(z)

# As you can see - the ALL 3 Instances are UNIQUE in Memory,
# regardless of the fact that we initialized it with the SAME 'url' value!

# But the Class is the UNIQUE object for ALL of its Instances!
assert x.__class__ is y.__class__ is z.__class__

# AND you have to be VERY CAREFUL of updating/deleting the Class attributes,
# because ALL Instances of the Class have "shared" access to their Class attributes!
