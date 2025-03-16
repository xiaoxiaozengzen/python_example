import os
import shutil
import subprocess
import re
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.env import VirtualRunEnv, VirtualBuildEnv
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.scm import Version

required_conan_version = ">=1.53.0"


class ExampleConan(ConanFile):
    name = "example"
    version = "dev"
    settings = "os", "compiler", "build_type", "arch"

    @property
    def _min_cppstd(self):
        return 14

    def configure(self):
        pass

    def requirements(self):
        self.requires("eigen/3.4.0")
        self.requires("pybind11/2.10.0")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_POLICY_DEFAULT_CMP0077"] = "NEW"
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()
        tc = VirtualRunEnv(self)
        tc.generate()
        tc = VirtualBuildEnv(self)
        tc.generate(scope="build")
