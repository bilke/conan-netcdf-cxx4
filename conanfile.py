from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration

class NetcdfcConan(ConanFile):
    name = "netcdf-cxx"
    version = "4.3.1"
    license = "MIT"
    author = "Lars Bilke, lars.bilke@ufz.de"
    url = "https://github.com/bilke/conan-netcdf-cxx"
    description = "Unidata network Common Data Form cxx"
    settings = "os", "compiler", "build_type", "arch"
    # options = {"shared": [True, False], "fPIC": [True, False]}
    # default_options = "shared=False", "fPIC=True"
    generators = "cmake"
    scm = {
        "type": "git",
        # "subfolder": "netcdf-cxx4",
        "url": "https://github.com/bilke/netcdf-cxx4.git",
        "revision": "fix-release-build"
     }

    def source(self):
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("CMakeLists.txt", "PROJECT(NCXX C CXX)",
                              '''PROJECT(NCXX C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def requirements(self):
        self.requires("netcdf-c/4.6.2@bilke/testing")

    # def config_options(self):
        # if self.settings.os == "Windows":
            # del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        # if self.settings.os == "Windows" and self.options.shared:
            # raise ConanInvalidConfiguration("Windows shared builds are not supported right now")

    def build(self):
        self.run('autoreconf -if')
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure()
        autotools.make()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["netcdf-cxx4"]

