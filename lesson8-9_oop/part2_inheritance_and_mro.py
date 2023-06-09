"""
Inheritance, Multiple Inheritance, MRO
"""

"""
Single Inheritance
"""
print("Inheritance: \n")


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def perimeter(self):
        return self.a + self.b + self.c

    def print_my_name(self):
        print(f"I'm Instance of the class {self.__class__.__name__}")


class Quadrangle(Triangle):
    def __init__(self, a, b, c, d):
        """
        Quadrangle is the child of Triangle, but for the Initialization
        of Quadrangle we need 4 arguments, not 3
        -- call the __init__ of parent class (Triangle) and set
           a, b, c to it
        -- set d as simple way (via 'self') because d is related to
        Quadrangle and NOT related to the Triangle
        """
        super().__init__(a, b, c)
        self.d = d

    def perimeter(self):
        """
        'perimeter' method is OVERLOADED: this means that
        CHILD class contains the method with the SAME name as
        its PARENT has, but with DIFFERENT implementation.

        This is needed for the Provision of the following to the SAME INTERFACE
        for PARENT and CHILD classes
        """
        return self.a + self.b + self.c + self.d


# ------------------------------------------------
triangle = Triangle(1, 2, 3)
print(triangle.perimeter())    # print the calculated perimeter related to the Triangle instance
quadrangle = Quadrangle(1, 2, 3, 4)
print(quadrangle.perimeter())  # print the calculated perimeter related to the Quadrangle instance

triangle.print_my_name()

# Quadrangle is CHILD of Triangle, and 'print_my_name' method was not overloaded in Quadrangle class,
# we can call PARENT method from the CHILD Instance.
# Here the method will print the Quadrangle class name for Quadrangle Instance
quadrangle.print_my_name()


"""
 Multiple Inheritance
"""
print("Multiple Inheritance: \n")


class Parent1:

    param = "Parent1 param"

    def get_parent1_name(self):
        print(Parent1.__name__)


class Parent2:

    param = "Parent2 param"

    def get_parent2_name(self):
        print(Parent2.__name__)


class Child(Parent1, Parent2):  # Child is INHERITED from Parent1 and Parent2

    param = "Child param"

    def __init__(self):
        self.param = "Child Instance param"


child = Child()
child.get_parent1_name()  # Call the Parent1 related method from Child Instance
child.get_parent2_name()  # Call the Parent2 related method from Child Instance

"""
 The MRO (Methods Order Resolution)
"""
mro = child.__class__.mro()
print(mro)  # print list where 1st element is the Child Class,
# 2 next elements are the Parent1 and Parent2 classes,
# and the last element is 'object' - because the 'object' is foremost PARENT of the ALL INSTANCES in Python
# NOTE: the 'type' is foremost PARENT of the ALL CLASSES in Python

# The Attributes Lookup Algorithm uses MRO for making lookup for the Attributes/Methods:

print("'param' value is " + child.param)
assert child.param == "Child Instance param"  # 'param' value is taken from Child Instance

del child.param   # Delete 'param' attribute from Child Instance
print("'param' value is " + child.param)
assert child.param == child.__class__.param  # 'param' value is taken from Child Class

del child.__class__.param  # Delete 'param' attribute from Child Class
first_parent = mro[1]
print(f"First parent is {first_parent}")
print("'param' value is " + child.param)
assert child.param == first_parent.param  # 'param' value is taken from the FIRST PARENT in MRO (Parent1 Class)

del first_parent.param  # Delete 'param' attribute from the FIRST PARENT in MRO (Parent1 Class)
second_parent = mro[2]
print(f"Second parent is {first_parent}")
print("'param' value is " + child.param)
assert child.param == second_parent.param  # 'param' value is taken from the SECOND PARENT in MRO (Parent2 Class)



