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
