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


class ArtdaqCoreDemo(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = (
        "https://github.com/art-daq/artdaq-core-demo/archive/refs/tags/v1_10_02.tar.gz"
    )
    git = "https://github.com/art-daq/artdaq-core-demo.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_05_00", commit="cfbeedf95665e881b5b42853360c767b5e779119")
    version("v2_04_00", commit="3f99a756c15a4dcadf8dfa1ba0a6fde45534c19e")
    version("v2_03_00", commit="9315a080486a660df17fa07e3f24609876c22d33")
    version("v2_02_00", commit="68ec3048288f7a0f5926a7bf2ffa734d3a522ce8")
    version("v2_01_00", commit="578abd4fb2e4ff9c497f8f55c4e547923677a01b")
    version("v2_00_00", commit="9831fd2fbe0091ac0458c6ce0b8af89b3cf85c4b")
    version("v1_12_00", commit="b751d08973539b787288c87f40dbac454a745031")
    version("v1_11_01", commit="4f5b040d6d43dc97033e0949bab27ecc2f6f16c2")
    version("v1_11_00", commit="3001d5f4dda9ee6f05609e7f99f90fe5ae81c6ea")
    version("v1_10_07", commit="459a63829b096fd84d2bb673587f1dd1f0720f95")
    version("v1_10_05", commit="8098e55fc42f1f2042419bb4a42063e58a544e03")
    version("v1_10_04", commit="6f0b0730c3077732d79ed2e02fdbe6eee6f5189b")
    version("v1_10_03", commit="20f691b6c1b093b7d9a513bf10ac26e9820b193a")
    version("v1_10_02", commit="aba71a8cae83b0cb32eecebebada1c1efcad0b4f")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq-core-demo/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v1_10_03",
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v1_10_04:",
    )
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("artdaq-core@:v3_99_00", when="@:v1_99_00")
    depends_on("artdaq-core@v4_00_00:,develop", when="@v2_00_00:,develop")
    depends_on("art-suite")

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
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
