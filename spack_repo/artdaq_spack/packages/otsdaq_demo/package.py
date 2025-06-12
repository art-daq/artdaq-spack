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


class OtsdaqDemo(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq-demo/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq-demo.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v3_02_00", commit="223a9b2203046322b4d1dd0b5125c8beb6ca4218")
    version("v3_01_00", commit="874580e1b40818270c4b4f9dc107c7ff0859e701")
    version("v3_00_00", commit="5f304b7f6ae03faba7cd0e749187d395c1985f35")
    version("v2_10_00", commit="d0c90f7a2b1114bfea0b64eb20cbdb9b40c4651e")
    version("v2_09_01", commit="9ad2e77fe82e8a0d3f11db0d3a5e7734bf6b0bfc")
    version("v2_09_00", commit="fa35f2c0c00cc84b82c0f567c88fb2405d53ea9c")
    version("v2_08_02", commit="4c4af9009475e00cacdd4fb8c700588f42366bab")
    version("v2_08_01", commit="0ea738a6f21c8678cc6c9d8f41ca1163ccb2cd18")
    version("v2_08_00", commit="677f1844f351c0ac5a481f484c54b8d0ea877191")
    version("v2_07_00", commit="6fcd7affda19c37908e4b204b4cc819b5e229593")
    version("v2_06_11", commit="6c5436d34d10c55842e7bd696e5e091239c1d158")
    version("v2_06_10", commit="71655c13c66d1502c418d3aaf9c692aa226b8733")
    version("v2_06_09", commit="ca9d6a82f25af382413f03ae46c5169aed6933c1")
    version("v2_06_08", commit="4c2aaa53e27ca6ef0a98bfaed0e66e4a9e2e6b34")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq-demo/archive/refs/tags/{0}.tar.gz"
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

    depends_on("otsdaq@:v2_99_00", when="@:v2_99_00")
    depends_on("otsdaq@v3_00_00:,develop", when="@v3_00_00:,develop")
    depends_on("otsdaq-utilities@:v2_99_00", when="@:v2_99_00")
    depends_on("otsdaq-utilities@v3_00_00:,develop", when="@v3_00_00:,develop")
    depends_on("otsdaq-components@:v2_99_00", when="@:v2_99_00")
    depends_on("otsdaq-components@v3_00_00:,develop", when="@v3_00_00:,develop")
    depends_on("artdaq-suite")

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
        env.set("OTSDAQ_DEMO_LIB", prefix.lib)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Ensure we can find libraries
        env.set("OTSDAQ_DEMO_LIB", prefix.lib)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
