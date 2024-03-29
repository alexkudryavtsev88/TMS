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
print(triangle.perimeter())
# print the calculated perimeter related to the Triangle instance
quadrangle = Quadrangle(1, 2, 3, 4)
print(quadrangle.perimeter())  # print the calculated perimeter related to the Quadrangle instance

triangle.print_my_name()

# Quadrangle is CHILD of Triangle, and 'print_my_name' method was not overloaded in Quadrangle class,
# we can call PARENT method from the CHILD Instance.
# Here the method will print the Quadrangle class name for Quadrangle Instance
quadrangle.print_my_name()