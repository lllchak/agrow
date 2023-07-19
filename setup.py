import os
from pathlib import Path
from enum import Enum
from typing import List

from Cython.Distutils import build_ext
from setuptools import (
    setup,
    Extension
)


SOURCE_EXTENSION = ".cc"
WRAPPER_EXTENSION = ".pyx"


def get_requirements() -> List[str]:
    with open("requirements.txt") as file:
        return [line.rstrip() for line in file]


def generate_extension(path: Path, package: str) -> Exception:
    module_name: str = get_module_name(package)

    return Extension(
        package + f".{module_name}",
        [
            os.path.join(path, f"core/{module_name}{SOURCE_EXTENSION}"),
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
        cmdclass={"build_ext": build_ext},
        ext_modules=EXTENSIONS,
        long_description="README.md",
        long_description_content_type="text/markdown"
    )
