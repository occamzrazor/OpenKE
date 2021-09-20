""""""

import platform

from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install


class custom_build_ext(build_ext):
    def build_extensions(self):
        self.compiler.set_executable("compiler_so", "g++")
        self.compiler.set_executable("compiler_cxx", "g++")
        self.compiler.set_executable("linker_so", "g++")
        build_ext.build_extensions(self)

    def get_ext_filename(self, ext_name):
        return f"{ext_name}.so"


class build_ext_first(install):
    def run(self):
        self.run_command("build_ext")
        super(build_ext_first, self).run()


PACKAGENAME = "openke"
VERSION = "2021.9.20"
PYTHON_REQUIRES = ">=3.9"
INSTALL_REQUIRES = [
    "setuptools",
    "torch>=1.9.0",
    "tqdm",
    "sklearn"
]

extra_compile_args = ["-fPIC", "-shared"]
extra_link_args = []

if platform.system() == 'Linux':
    try:
        if platform.architecture()[0] == '64bit':
            extra_compile_args = ['-pthread']
        else:
            extra_compile_args = ['-pthread', '-march=pentium4']
    except KeyError:
        extra_compile_args = ['-pthread', '-march=pentium4']
    extra_link_args = ['-pthread']

setup(
    name=PACKAGENAME,
    version=VERSION,
    description="OpenKE: An Open Toolkit for Knowledge Embedding",
    url="git@github.com:occamzrazor/OpenKE.git",
    author="Han, Xu and Cao, Shulin and Lv Xin and Lin, Yankai and Liu, Zhiyuan and Sun, Maosong and Li, Juanzi",
    packages=find_packages(exclude=["benchmarks", "examples"]),
    ext_modules=[
        Extension(
            "openke/release/Base",
            sources=["openke/base/Base.cpp"],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args
        )
    ],
    zip_safe=False,
    cmdclass={
        "install": build_ext_first,
        "build_ext": custom_build_ext,
    },
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)
