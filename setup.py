import os
from pathlib import Path
from enum import Enum
from typing import List

from Cython.Distutils import build_ext
from setuptools import (
    setup,
    Extension
)


AUTHOR = "Pavel Lyulchak"
EMAIL = "mediumchak@yandex.ru"
LICENSE = "MIT Licence"
NAME = "agrow"
VERSION = "0.1"
# keep in sync with github description
DESCR = "Python framework for solving math & NLP (Natural Language Processing) tasks"
# add PyPi url after package deploy
URL = ""

C_SOURCE_EXTENSION = ".c"
WRAPPER_EXTENSION = ".pyx"


def get_requirements() -> List[str]:
    with open("requirements.txt") as file:
        return [line.rstrip() for line in file]


def generate_extension(path: Path, package: str) -> Exception:
    module_name: str = get_module_name(package)

    return Extension(
        package + f".{module_name}",
        [
            os.path.join(path, f"core/{module_name}{C_SOURCE_EXTENSION}"),
            os.path.join(path, f"{module_name}{WRAPPER_EXTENSION}")
        ]
    )


def get_module_name(package: str) -> str:
    return package.split('.')[-1]


class BuildPackages(Enum):
    MATH_FUNC = ("agrow.math.func", Path("agrow/math/func"))  # agrow.math.func

    @classmethod
    def values(cls):
        return list(map(lambda path: path.value, cls))


PACKAGES_INFO = [package_info for package_info in BuildPackages.values()]
EXTENSIONS = [generate_extension(path, package) for package, path in PACKAGES_INFO]


if __name__ == "__main__":
    setup(
        install_requires=get_requirements(),
        packages=[p for p, _, in PACKAGES_INFO],
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
