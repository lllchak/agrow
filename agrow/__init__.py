import sys


if sys.version_info < (3,):
    raise Exception(
        "Python 2 is not supported by AgRow. "
        "You can install actual Python version at python.org"
    )

from .core import *

__all__ = core.__all__
