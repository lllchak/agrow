from setuptools import setup, Extension
from Cython.Distutils import build_ext

def make_package_from_path(path: str) -> str:
    return '.'.join(path.split('/'))

AUTHOR = "Pavel Lyulchak"
EMAIL = "mediumchak@yandex.ru"

NAME = "agrow"
VERSION = "0.1"
DESCR = "A small template project that shows how to wrap C/C++ code into python using Cython"
URL = ""

with open("requirements.txt") as file:
    reqs = [line.rstrip() for line in file]

REQUIRES = reqs

LICENSE = "MIT Licence"

MATH_FUNC_DIR = "agrow/math/func"
PACKAGES = [
    make_package_from_path(MATH_FUNC_DIR)
]

EXTENSIONS = [
    # agrow.math.func
    Extension(
        '.'.join(MATH_FUNC_DIR.split('/')) + ".func", 
        [MATH_FUNC_DIR + "/core/func.c", MATH_FUNC_DIR + "/func.pyx"]
    )
]

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
