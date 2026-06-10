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


class ArtdaqCore(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq-core/archive/refs/tags/v3_09_04.tar.gz"
    git = "https://github.com/art-daq/artdaq-core.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v5_03_00", commit="77de74f69ced6f1e3fd988569367b4402e239870")
    version("v5_02_00", commit="0e75b70486fde6e891d99879fa653bc339f55d3f")
    version("v5_01_00", commit="5c46776217ce5f215e0164f1485c29afc407e45b")
    version("v5_00_00", commit="0fc9cb660abfaa73d4812a553c67bfafebc0a0db")
    version("v4_03_00", commit="5f18a19a36c85aeb4c05ad29b8421e96497b4531")
    version("v4_02_00", commit="49c4220914a9c46745e3a387a8163438db473a81")
    version("v4_01_00", commit="fe45771437e086f2b6ca85c01237b426c1b3f09e")
    version("v4_00_00", commit="12d6d49e14e50b009ffde0329f936ed00d22fe0e")
    version("v3_13_00", commit="75fb6a28438ff4a9a74dc9128c5bc05b11ae97f4")
    version("v3_12_00", commit="34d404d42b6d9bf3ae33b20aebd1fa6fc404a409")
    version("v3_11_01", commit="8bfc8d99f528ce36cb6faaca627090a329959596")
    version("v3_11_00", commit="5dcbc0400e6bedd10f43e8201e7fc32fff0be5a9")
    version("v3_10_03", commit="32e7447b789e6e1a376ff9e1653e2e5510e8dcc1")
    version("v3_10_02", commit="aec92f2c0d0889e14f60e089eb2326e42b6bf2a0")
    version("v3_10_01", commit="7d6acf8b30342e1046ae9efdfd3d1b85ba678834")
    version("v3_09_16", commit="5fc67595e2871b8157bbf60a0a215ffeb9314957")
    version("v3_09_15", commit="90073303ffafcc01f559b43bacbeadf661ac63da")
    version("v3_09_13", commit="bb7b98d33fa2c1663e11e343aa76fb2e10f8bc67")
    version("v3_09_12", commit="87f229423aea7a27781376508033ef5e15802b5d")
    version("v3_09_11", commit="36319c2b608ade91d77e679bf4bb423e93d18cd9")
    version("v3_09_09", commit="0550f8bbab6912ffdef4f898ccd3800afb136539")
    version("v3_09_08", commit="9f04cacde9be1e327e79fa401d5f504c6cd23e4c")
    version("v3_09_07", commit="23348fa245e46096c9b7a8fc81b553850a2a64ea")
    version("v3_09_04", commit="d15bf64341f4576ab475d5a151ac22894d2ee363")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v3_09_11",
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v3_09_12:",
    )
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("doc", default=False, description="Build documentation with Doxygen.")
    variant(
        "bundle",
        default=True,
        sticky=True,
        description="Use the art-suite bundle to fix dependency versions",
    )

    # art dependencies
    depends_on("canvas-root-io cxxstd=17", when="cxxstd=17")
    depends_on("canvas-root-io cxxstd=20", when="cxxstd=20")
    depends_on("art-suite", when="+bundle")
    depends_on("cetmodules@3.26.00:", type="build")

    # artdaq dependencies
    depends_on("trace+mf")
    depends_on("doxygen", when="+doc")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq-core/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        if os.path.exists("CMakePresets.cmake"):
            args.extend(["--preset", "default"])
        else:
            self.define("artdaq_core_OLD_STYLE_CONFIG_VARS", True)
        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies("~doc"):
            env.set("DISABLE_DOXYGEN", 1)

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
