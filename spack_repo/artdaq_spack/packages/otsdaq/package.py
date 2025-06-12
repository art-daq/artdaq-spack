# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class Otsdaq(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v3_02_00", commit="6c2518b75e6909ebd9739b444666b1833e246edc")
    version("v3_01_00", commit="d82822db1da643907cc049803dbd7fa3c034c370")
    version("v3_00_00", commit="9aa0eb11ac827f4d9b1bdc3d08fbb8edd1f14fcb")
    version("v2_10_00", commit="929310452541e91c4a4a3170bf1b05cc1cb64937")
    version("v2_09_01", commit="6adeb565170e4c137923283897de3c276e6d9d68")
    version("v2_09_00", commit="20b531aef65c3296f86f522934ff45bb0bd6f8ff")
    version("v2_08_02", commit="a84bc01f80e763253184393f61303449719801e8")
    version("v2_08_01", commit="d9d0cad63a49f0bdbc61ce7b64e28ad96b31cc9c")
    version("v2_08_00", commit="356d88a88a704cae7683686eccd251fe8e4a527f")
    version("v2_07_00", commit="bc74ed21db7ac4127ffb3d988d7fa87c17fde1fe")
    version("v2_06_11", commit="48e4d6539d92c296b1a6691e4ab01a1a75056b62")
    version("v2_06_10", commit="5061d7b4314f634f04bf9b2e16edc28dbe430efd")
    version("v2_06_09", commit="6f303ad35597bb7dd63da4d5c9e60af648bcaced")
    version("v2_06_08", commit="6238ece959487388b0191280fe989f7f9e584546")
    version("v2_06_07", commit="ccacb68435536b386832b3ba7ab19509eafb05e7")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v2_06_09"
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v2_06_10:"
    )
    depends_on("cxx", type="build")

    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("xdaq")
    depends_on("reredirect", when="@v2_09_00:")

    depends_on("artdaq@:v3_99_00", when="@:v2_99_00")
    depends_on("artdaq@v4_00_00:,develop", when="@v3_00_00:,develop")
    depends_on("artdaq-database~builtin_fhicl")
    depends_on("artdaq-database@:v1_99_00", when="@:v2_99_00")
    depends_on("artdaq-database@v2_00_00:,develop", when="@v3_00_00:,develop")
    depends_on("artdaq-daqinterface@:v3_99_00", when="@:v2_99_00")
    depends_on("artdaq-daqinterface@v4_00_00:,develop", when="@v3_00_00:,develop")
    depends_on("artdaq-suite")

    depends_on("artdaq cxxstd=20", when="cxxstd=20")
    depends_on("artdaq cxxstd=17", when="cxxstd=17")

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
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Ensure we can find libraries
        env.set("OTSDAQ_LIB", prefix.lib)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Ensure we can find libraries
        env.set("OTSDAQ_LIB", prefix.lib)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
