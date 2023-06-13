import dataclasses
from typing import Type, Any


@dataclasses.dataclass
class DescriptorMethod:
    GET = "__get__"
    SET = "__set__"
    DELETE = "__delete__"


class NonDataDescriptor:
    def __get__(self, instance, owner):
        return f"Retrieving from '__get__' method of 'NonData Descriptor'"

    def __str__(self):
        return f"NonDataDescriptor class <id: {id(self)}>"


class DataDescriptor:
    def __get__(self, instance, owner):
        return f"Retrieving from '__get__' method of 'DataDescriptor'"

    def __set__(self, instance, value):
        pass

    def __str__(self):
        return f"DataDescriptor class <id: {id(self)}>"


class ClassWithDataDescriptor:
    cls_data_descriptor_field = DataDescriptor()

    def __str__(self):
        return f"ClassWithDataDescriptor class <id: {id(self)}>"


class ClassWithNonDataDescriptor:
    cls_non_data_descriptor_field = NonDataDescriptor()

    def __str__(self):
        return f"ClassWithNonDataDescriptor class <id: {id(self)}>"

# ------------------------------------------------
# object.getattribute() impl
# ------------------------------------------------


def _mro_getattr(type_: Type, attr: str) -> Any:
    """Get an attribute from a type based on its MRO."""
    for base in type_.mro():
        if attr in base.__dict__:
            return base.__dict__[attr]
    else:
        raise AttributeError(f"{type_.__name__!r} object has no attribute {attr!r}")


class MyType:

    def __getattribute__(self, attr: str, /) -> Any:
        """Attribute access."""
        # Objects/object.c: PyObject_GenericGetAttr

        if not isinstance(attr, str):
            raise TypeError(
                f"attribute name must be string, not {type(attr).__name__!r}"
            )

        type_attr = descriptor_type_get = None
        # get a type (class) of current Instance
        self_type = type(self)

        try:
            # search for Attribute in Instance's Class and its parent Classes (by MRO)
            type_attr = _mro_getattr(self_type, attr)
        except AttributeError:
            pass  # the Attribute wasn't found in Instance's Class and its parent Classes
        else:
            # get a Class of found Instance's Class Attribute
            type_attr_class = type(type_attr)
            try:
                # search for '__get__' method in Class of found Instance's Class Attribute
                descriptor_type_get = _mro_getattr(type_attr_class, DescriptorMethod.GET)
            except AttributeError:
                pass  # the Attribute is not a Descriptor, but it's a Class Attribute.
            else:
                # the Attribute is at least a Non-Data Descriptor.
                for base in type_attr_class.mro():
                    attr_dict = base.__dict__
                    if DescriptorMethod.SET in attr_dict or DescriptorMethod.DELETE in attr_dict:
                        # the Attribute is a Data Descriptor (1st Priority level)
                        return descriptor_type_get(type_attr, self, self_type)

        if attr in self.__dict__:
            # the Attribute is an Instance Attribute (2nd Priority level)
            return self.__dict__[attr]
        elif descriptor_type_get is not None:
            # the Attribute is a Non-Data Descriptor (3rd Priority level)
            return descriptor_type_get(type_attr, self, self_type)
        elif type_attr is not None:
            # the Attribute is a Class Attribute (4th Priority level)
            return type_attr
        else:
            raise AttributeError(f"{self.__name__!r} object has no attribute {attr!r}")


class MyClass(MyType, ClassWithDataDescriptor, ClassWithNonDataDescriptor):
    cls_simple_field = "class_simple_field"

    def __init__(self):
        self.obj_non_data_descriptor_field = NonDataDescriptor()
        self.obj_data_descriptor_field = DataDescriptor()
        self.obj_simple_field = "obj_simple_field"

    @property
    def property_field(self):
        return "property_field"

    def __str__(self):
        return "<Bar class>"


# my_class = MyClass()
# print(f"Class Data Descriptor field: {my_class.cls_data_descriptor_field}")
# print(f"Class Non-Data Descriptor field: {my_class.cls_non_data_descriptor_field}")
# print(f"Class simple field: {my_class.cls_simple_field}")
#
# print(f"Property field: {my_class.property_field}")
#
# print(f"Instance Data Descriptor field: {my_class.obj_data_descriptor_field}")
# print(f"Instance Non-Data Descriptor field: {my_class.obj_non_data_descriptor_field}")
# print(f"Instance simple field: {my_class.obj_simple_field}")

