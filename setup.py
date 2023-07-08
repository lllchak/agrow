from setuptools import setup, Extension
from Cython.Distutils import build_ext

NAME = "agrow"
VERSION = "0.1"
DESCR = "A small template project that shows how to wrap C/C++ code into python using Cython"
URL = ""

with open("requirements.txt") as file:
    reqs = [line.rstrip() for line in file]

REQUIRES = reqs

AUTHOR = "Pavel Lyulchak"
EMAIL = "mediumchak@yandex.ru"

LICENSE = "MIT Licence"

MATH_FUNC_DIR = "agrow/math/func"
PACKAGES = ['.'.join(MATH_FUNC_DIR.split('/'))]

math_func_ext = Extension(
    '.'.join(MATH_FUNC_DIR.split('/')) + ".wrapped",
    [MATH_FUNC_DIR + "/core/func.c", MATH_FUNC_DIR + "/wrapped.pyx"]
)

EXTENSIONS = [math_func_ext]

if __name__ == "__main__":
    setup(
        install_requires=REQUIRES,
        packages=PACKAGES,
        zip_safe=False,
        name=NAME,
        version=VERSION,
        description=DESCR,
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        license=LICENSE,
        cmdclass={"build_ext": build_ext},
        ext_modules=EXTENSIONS
    )
