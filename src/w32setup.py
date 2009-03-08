
from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')
setup(
options = {'py2exe':{'excludes':['OpenGL'],#,'pygame'],

                     'packages':['ctypes','logging','weakref'],
                     'includes':['new','distutils.util']}},
#                     'bundle_files':1}},
console = ["main.py"],
)
