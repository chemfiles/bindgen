"""
Various constants for Python FFI generation
"""

LICENCE = """# Chemfiles, a modern library for chemistry file reading and writing
# Copyright (C) Guillaume Fraux and contributors -- BSD license
"""

BEGINING = (
    LICENCE
    + """#
# =========================================================================== #
# !!!! AUTO-GENERATED FILE !!!! Do not edit. See the bindgen repository for
# the generation code (https://github.com/chemfiles/bindgen).
# This file contains Python ctype interface to the C API
# =========================================================================== #
"""
)
