from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration

class NetcdfcConan(ConanFile):
    name = "netcdf-cxx"
    version = "4.3.1-2"
    license = "MIT"
    author = "Lars Bilke, lars.bilke@ufz.de"
    url = "https://github.com/bilke/conan-netcdf-cxx"
    description = "Unidata network Common Data Form cxx"
    settings = "os", "compiler", "build_type", "arch"
    # options = {"shared": [True, False], "fPIC": [True, False]}
    # default_options = "shared=False", "fPIC=True"
    generators = "cmake"

    def source(self):
        self.run("git clone --depth=1 https://github.com/Unidata/netcdf-cxx4.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("netcdf-cxx4/CMakeLists.txt", "PROJECT(NCXX C CXX)",
                              '''PROJECT(NCXX C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        # Fix usage of custom FindHDF5.cmake in hdf5 package
        # Also: Fix NO_MODULES to NO_MODULE, removed link type
        tools.replace_in_file("netcdf-cxx4/CMakeLists.txt",
            "FIND_PACKAGE(HDF5 NAMES ${SEARCH_PACKAGE_NAME} COMPONENTS C HL NO_MODULES REQUIRED ${NC_HDF5_LINK_TYPE})",
            '''set(HDF5_DIR ${CONAN_HDF5_ROOT}/cmake/hdf5)
      FIND_PACKAGE(HDF5 REQUIRED COMPONENTS C HL NO_MODULE)''')

    def requirements(self):
        self.requires("netcdf/4.7.4")

    # def config_options(self):
        # if self.settings.os == "Windows":
            # del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        # if self.settings.os == "Windows" and self.options.shared:
            # raise ConanInvalidConfiguration("Windows shared builds are not supported right now")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["NCXX_ENABLE_TESTS"] = False
        cmake.definitions["ENABLE_CONVERSION_WARNINGS"] = False
        cmake.definitions["BUILD_SHARED_LIBS"] = False
        cmake.configure(source_folder="netcdf-cxx4")
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["netcdf-cxx4"]

