import subprocess

from setuptools import find_namespace_packages, setup, Extension
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
VERSION = "2021.9.15"
PYTHON_REQUIRES = ">=3.9"
INSTALL_REQUIRES = [
    "setuptools",
    "torch==1.9.0",
]

setup(
    name=PACKAGENAME,
    version=VERSION,
    description="OpenKE: An Open Toolkit for Knowledge Embedding",
    url="git@github.com:occamzrazor/OpenKE.git",
    author="Han, Xu and Cao, Shulin and Lv Xin and Lin, Yankai and Liu, Zhiyuan and Sun, Maosong and Li, Juanzi",
    author_email="admin@occamzrazor.com",
    license="",
    packages=find_namespace_packages(exclude=["examples", "benchmarks"], include=["openke/**"]),
    #package_dir={"": "."},
    #package_data={"": ["openke/release/Base.so"]},
    ext_modules=[
        Extension(
            "openke.release.Base",
            sources=["openke/base/Base.cpp"],
            extra_compile_args=["-fPIC", "-shared"],
        )
    ],
    zip_safe=False,
    cmdclass={
    #    "install": build_ext_first,
        "build_ext": custom_build_ext,
    },
    #include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)
