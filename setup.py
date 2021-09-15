from setuptools import find_namespace_packages, setup, Extension, command


class custom_build_ext(command.build_ext.build_ext):
    def build_extensions(self):
        self.compiler.set_executable("compiler_so", "g++")
        self.compiler.set_executable("compiler_cxx", "g++")
        self.compiler.set_executable("linker_so", "g++")
        command.buil_ext.build_ext.build_extensions(self)

    def get_ext_filename(self, ext_name):
        return f"{ext_name}.so"

class Build_ext_first(command.install.install):
    def run(self):
        self.run_command("build_ext")
        super(Build_ext_first, self).run()

PACKAGENAME = "OpenKE"
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
    packages=find_namespace_packages(exclude=["examples", "benchmarks"], include=["openke"]),
    ext_modules=[
        Extension(
            "Base",
            sources=["openke/base/Base.cpp"],
            extra_compile_args=["-fPIC", "-shared"],
        )
    ],
    zip_safe=False,
    cmdclass={
        'install': Build_ext_first,
        "build_ext": custom_build_ext,
    },
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)
