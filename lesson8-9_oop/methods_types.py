"""
super() and methods overriding
"""


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def perimeter(self):
        return self.a + self.b + self.c


class Quadrangle(Triangle):
    def __init__(self, a, b, c, d):
        """
        Так как Quadrangle является наледником Triangle, но
        для его инициализации нужно 4 переменных, а не 3:
        -- вызываем __init__ у РОДИТЕЛЬСКОГО класса через super(),
           и передаем в этот __init__ первые 3 переменные
        -- 4-ю переменную сетаем обыкновенным образом через
           self.variable = variable
        """
        super(Quadrangle, self).__init__(a, b, c)
        self.d = d

    def perimeter(self):
        return self.a + self.b + self.c + self.d

# ------------------------------------------------

"""
__new__() overriding: Singleton pattern example
"""

class Singleton:
    """
    Паттерн Singleton разрешает создать ровно 1 Экземпляр указанного Класса
    - При попытке создать еще один Экземпляр - вернется ссылка на уже существующий Экземпляр
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


s1, s2, s3 = Singleton(), Singleton(), Singleton()
assert s1 is s2 and s1 is s3 and s2 is s3
# Адреса в памяти s1, s2 и s3 - одинаковы, так как это все ровно 1 Объекта

"""
classmethod, staticmethod, property
"""

class MyClass:
    NAME = None

    @property
    def name(self):
        """
        property:
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
        cls.NAME = name  # здесь NAME - переменная уровня КЛАССА

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



MyClass.set_name("Alex")       # вызов classmethod от имени КЛАССА, до создания Экземпляра
my_class_instance = MyClass()   # создание Экземпляра КЛАССА
MyClass.print_hello()            # вызов staticmethod от имени КЛАССА
my_class_instance.print_hello()   # вызов staticmethod от имени Экземпляра
print(my_class_instance.name)     # вызов property через обращение к атрибуту Экземпляра с именем name


"""
Описать Dataclass, который 
- содержит три произвольных поля, разных типов
- имеет один-единственный classmethod, который проверяет типы 
этих трех полей и возвращает объект Dataclass'a
- является НЕизменяемым (у объекта этого класса нельзя изменить  
значения атрибута/добавить новый атрибут после его создания)
"""


