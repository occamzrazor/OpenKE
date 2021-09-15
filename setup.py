from setuptools import find_namespace_packages, setup, Extension
from setuptools.command.build_ext import build_ext


class custom_build_ext(build_ext):
    def build_extensions(self):
        # Override the compiler executables. Importantly, this
        # removes the "default" compiler flags that would
        # otherwise get passed on to to the compiler, i.e.,
        # distutils.sysconfig.get_var("CFLAGS").
        self.compiler.set_executable("compiler_so", "g++")
        self.compiler.set_executable("compiler_cxx", "g++")
        self.compiler.set_executable("linker_so", "g++")
        build_ext.build_extensions(self)

    def get_ext_filename(self, ext_name):
        return f"{ext_name}.so"

PACKAGENAME = "OpenKE"
VERSION = "2021.9.15"
PYTHON_REQUIRES = ">=3.8"
INSTALL_REQUIRES = [
    "setuptools",
]

setup(
    name=PACKAGENAME,
    version=VERSION,
    description="OpenKE: An Open Toolkit for Knowledge Embedding",
    url="git@github.com:occamzrazor/OpenKE.git",
    author="Han, Xu and Cao, Shulin and Lv Xin and Lin, Yankai and Liu, Zhiyuan and Sun, Maosong and Li, Juanzi",
    author_email="admin@occamzrazor.com",
    license="",
    packages=find_namespace_packages(),
    ext_modules=[
        Extension(
            "Base",
            sources=["openke/base/Base.cpp"],
            extra_compile_args=["-fPIC", "-shared"],
        )
    ],
    zip_safe=False,
    cmdclass={"build_ext": custom_build_ext },
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)
