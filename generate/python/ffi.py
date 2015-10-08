# -* coding: utf-8 -*

"""
This module generate the Fortran interface declaration for the functions it
finds in a C header. It only handle edge cases for the chemfiles.h header.
"""
from .constants import BEGINING
from .convert import type_to_python

from generate.ctype import StringType
from generate.functions import TYPES

BEGINING += """
'''
Foreign function interface declaration for the Python interface to chemfiles
'''

import sys

from numpy.ctypeslib import ndpointer
import numpy as np
from ctypes import *

from .errors import _check
from .find_chemfiles import find_chemfiles


class ChemfilesLibrary(object):
    def __init__(self):
        self._cache = None

    def __call__(self):
        if self._cache is None:
            self._cache = find_chemfiles()
            set_interface(self._cache)
        return self._cache

get_c_library = ChemfilesLibrary()
"""


CLASS_TEMPLATE = """

class {name}(Structure):
    pass
"""

ENUM_TEMPLATE = """

class {name}(c_int):
    {values}
"""

FUNCTION_TEMPLATE = """
    # Function "{name}", at {coord}
    c_lib.{name}.argtypes = {argtypes}
    c_lib.{name}.restype = {restype}
    {errcheck}
"""


def interface(function):
    '''Convert a function interface to Ctypes'''
    args = [type_to_python(arg.type, cdef=True) for arg in function.args]
    argtypes = "[" + ", ".join(args) + "]"
    restype = type_to_python(function.rettype)

    if restype == "c_int":
        errcheck = "c_lib." + function.name + ".errcheck = _check"
    else:
        errcheck = ""
    return FUNCTION_TEMPLATE.format(name=function.name,
                                    coord=function.coord,
                                    argtypes=argtypes,
                                    restype=restype,
                                    errcheck=errcheck)


def wrap_enum(enum):
    '''Wrap an enum'''
    values = []
    i = 0
    for e in enum.enumerators:
        if e.value is None:
            value = i
            i += 1
        else:
            value = e.value.value
        values.append(str(e.name) + " = " + str(value))
    return ENUM_TEMPLATE.format(name=enum.name, values="\n    ".join(values))


def write_ffi(filename, enums, functions):
    with open(filename, "w") as fd:
        fd.write(BEGINING)

        for enum in enums:
            fd.write(wrap_enum(enum))

        for name in TYPES:
            fd.write(CLASS_TEMPLATE.format(name=name))

        fd.write("\n\ndef set_interface(c_lib):")
        for func in functions:
            fd.write(interface(func))
