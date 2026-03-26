# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class OtsdaqUtilities(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = (
        "https://github.com/art-daq/otsdaq-utilities/archive/refs/tags/v2_06_08.tar.gz"
    )
    git = "https://github.com/art-daq/otsdaq-utilities.git"

    version("develop", branch="develop", get_full_repo=True, submodules=True)
    version("v3_06_00", commit="fbfe837b0423c6c39b89ea400405f070d263d122")
    version("v3_05_00", commit="365b927f149f4efd6ecfda7cd06632cfad82b435")
    version("v3_04_01", commit="0070748eaf3f7fe86deae2f0aecca1ed1e905abe")
    version("v3_04_00", commit="09b76e7d98ff8b9e964352b86fc653dca198488d")
    version("v3_03_02", commit="96d8123c75dab05ca666d704435d4bff906dfa3a")
    version("v3_03_01", commit="18b86eab322028bd8f824f53bef1a0b5db940792")
    version("v3_03_00", commit="ebf2d0e8d5756ac478f941d43bc72aca29bcbdfc")
    version("v3_02_00", commit="c10d818287c80f02dd7204440d8440cadf5b7573")
    version("v3_01_00", commit="8841fc807a36e74980c12a38094a4f9fc8fd336e")
    version("v3_00_00", commit="a29dbfdae1569b8a5c737d0c9e14783db1105e59")
    version("v2_10_00", commit="15d657c38c538facc92c4d40d0ecf25c8b580cb7")
    version("v2_09_01", commit="c2ad94dfc9eb42f62e32c164f6a63e6933f02b4c")
    version("v2_09_00", commit="3d21943cdcc72631f56d4b5002769fa84c255ed3")
    version("v2_08_02", commit="1f159f22d7cb4fa441524254e06024a7e0548451")
    version("v2_08_01", commit="d4eefb566bb14effb9521d3baa27b955e2434598")
    version("v2_08_00", commit="85559270d5aa0ee6d40c2d39b3e7cc4c49e3fcb9")
    version("v2_07_00", commit="d601f6d71de67d9845e066b0d98b4b7f257d1b1f")
    version("v2_06_11", commit="ebcfa9f605dd40583b53a2c16c49ae19eaa7445d")
    version("v2_06_10", commit="88e8683f505a031f1d43ac03b9ace916fc980409")
    version("v2_06_09", commit="ef01560eaac07df1cf2fde6a3756e625e272959d")
    version("v2_06_08", commit="e02546704301d7506bec0fe842ac9789e57d9f43")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq-utilities/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v2_06_09",
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v2_06_10:",
    )
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules@3.26.00:", type="build")

    depends_on("otsdaq@:v2_99_00", when="@:v2_99_00")
    depends_on("otsdaq@v3_00_00:,develop", when="@v3_00_00:,develop")
    depends_on("artdaq-suite")

    #    depends_on("xsd") #for ECLWriter
    depends_on("curl")  # for ECLWriter
    depends_on("py-slack-sdk")  # For ChatSupervisor
    depends_on("cppzmq")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        if os.path.exists("CMakePresets.cmake"):
            args.extend(["--preset", "default"])
        else:
            self.define("artdaq_core_OLD_STYLE_CONFIG_VARS", True)
        return args

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find WebGUI Data
        env.set("OTSDAQ_UTILITIES_DIR", prefix)
        # Ensure we can find libraries
        env.set("OTSDAQ_UTILITIES_LIB", prefix.lib)

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find WebGUI Data
        env.set("OTSDAQ_UTILITIES_DIR", prefix)
        # Ensure we can find libraries
        env.set("OTSDAQ_UTILITIES_LIB", prefix.lib)
