import abc


class AbstractClassNoABC:

    @abc.abstractmethod
    def some_method(self):
        pass


class AbstractClassABC(abc.ABC):

    @abc.abstractmethod
    def some_method(self):
        pass


class MyClass1(AbstractClassNoABC):

    def another_method(self):
        pass


class MyClass2(AbstractClassABC):

    def another_method(self):
        pass


class MyClass3(AbstractClassABC):

    def another_method(self):
        pass

    def some_method(self):
        print("Hello world!")


for cls_ in (MyClass1, MyClass2, MyClass3):
    try:
        instance = cls_()
        print(f"Created instance: {instance}")
    except Exception as exc:
        print(f"ERROR: {exc}")

