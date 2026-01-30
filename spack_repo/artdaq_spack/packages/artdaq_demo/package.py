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

class ArtdaqDemo(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq-demo/archive/refs/tags/v3_12_02.tar.gz"
    git = "https://github.com/art-daq/artdaq-demo.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v4_05_00", commit="6650f44018cc624675f9104be9cb56b62b3a68d9")
    version("v4_04_00", commit="8a4c861c212340c2e7cf6612e7d56b671d759d24")
    version("v4_03_00", commit="d4b3f968134d3ac1edac51aee0f86db4af5923cb")
    version("v4_02_00", commit="5b9423b5ab10f7e91b91f181a44fb1344f126e2c")
    version("v4_01_00", commit="e6f580e9ed1bed86b67280e0b5d6d32165f96643")
    version("v4_00_00", commit="3d7ab3a16bcf9eb71469a83e908b73f91f00f5ce")
    version("v3_16_00", commit="ece227114da3fc374c9c04446e01182b8b49bb1c")
    version("v3_15_00", commit="05d4b2c9bebe74a4e71de232ba9a1ae020d78f62")
    version("v3_14_01", commit="aaa8cc5cb2b7efc3544195e09d63c7db6d9f320c")
    version("v3_14_00", commit="2e67f04e7fac6b7ab6d6896c0df0316b3122ab1b")
    version("v3_13_01", commit="3bb72231d2196be8efd028b6137070e6ca2dcd60")
    version("v3_13_00", commit="a0255fe443765839448664c915b542b0419c0c7d")
    version("v3_12_07", commit="d608307d9005839aef29cf8b675e774090e82e41")
    version("v3_12_05", commit="cfd39c01b69feb21674b4ba6ec221d3999f371e2")
    version("v3_12_04", commit="07116b927b7b5da3f08ed03e1821bac8e9f3e2ab")
    version("v3_12_03", commit="afbe8740573e0c324244ae7eb238b7fa16d923e0")
    version("v3_12_02", commit="082d1df470d7f826801c10c5f3b1e844e110c1a4")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq-demo/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v3_12_03"
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v3_12_04:"
    )
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules@3.26.00:", type="build")

    depends_on("artdaq@:v3_99_00", when="@:v3_99_00")
    depends_on("artdaq@v4_00_00:,develop", when="@v4_00_00:,develop")
    depends_on("artdaq-core-demo@:v1_99_00", when="@:v3_99_00")
    depends_on("artdaq-core-demo@v2_00_00:,develop", when="@v4_00_00:,develop")
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
