#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


cext_module = Extension('_cext',
                        sources=['cext_wrap.c', 'cext.c'],
                        )

setup (name = 'cext',
       version = '0.96',
       author      = "Sergio Gonzalez",
       description = """Optimize pyCave""",
       ext_modules = [cext_module],
       py_modules = ["cext"],
       )
