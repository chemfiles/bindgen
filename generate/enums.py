# -* coding: utf-8 -*
from pycparser import c_ast


class Enumerator:
    '''A value in a enum'''
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Enum:
    '''Class representing a C enum'''

    def __init__(self, name):
        self.name = name
        self.enumerators = []

    def append(self, name, value=None):
        '''
        Append a name in the enum list, with optional value
        '''
        self.enumerators.append(Enumerator(name, value))

    def __str__(self):
        res = "enum " + self.name + " { \n"
        for enumerator in self.enumerators:
            res += "    " + enumerator.name
            if enumerator.value is not None:
                res += " = " + enumerator.value
            res += "\n"
        res += "}"
        return res

    def __repr__(self):
        return str(self)


ENUM_NAMES = {
    "CHFL_SUCCESS": "chfl_status",
    "CHFL_CELL_ORTHORHOMBIC": "chfl_cellshape",
    "CHFL_PROPERTY_BOOL": "chfl_property_kind",
    "CHFL_BOND_UNKNOWN": "chfl_bond_order",
}


class EnumsVisitor(c_ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super(EnumsVisitor, self).__init__(*args, **kwargs)
        self.enums = []

    def visit(self, *args, **kwargs):
        super(EnumsVisitor, self).visit(*args, **kwargs)
        return self.enums

    def visit_Enum(self, node):
        first_value = node.values.enumerators[0].name
        name = ENUM_NAMES[first_value]
        enum = Enum(name)
        for enumerator in node.values.enumerators:
            enum.append(enumerator.name, enumerator.value)
        self.enums.append(enum)
