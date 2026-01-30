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

class ArtdaqEpicsPlugin(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq-epics-plugin/archive/refs/tags/v1_05_02.tar.gz"
    git = "https://github.com/art-daq/artdaq-epics-plugin.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_01_00", commit="36d095273ffa4907fc37f9392594e90bde98b3ab")
    version("v2_00_00", commit="fedb5fd92785467df7652374333a3396377c312c")
    version("v1_07_00", commit="21dd76ab9b73ad3293f33ecce0e73d227472c853")
    version("v1_06_03", commit="c3d8bf7b686adeee4dbffec97ad9b8a9e8902255")
    version("v1_06_02", commit="5f4bc2056c51b0b1c84322d91866d29378e9739e")
    version("v1_06_01", commit="7da37d4f86fbd37fe666aba4f7e80b3240daa678")
    version("v1_06_00", commit="7fb149d0dedf5216d29b03359738d5b21f59680a")
    version("v1_05_06", commit="e0542cc88bb0da25ac875552ba1fa45a1e28ce95")
    version("v1_05_04", commit="e68e85038ff75b6d2c1fb60ef11d4f6683f7241d")
    version("v1_05_03", commit="a6d75ec3f4523b53aabfd5c9ed7419ae0c2cef5b")
    version("v1_05_02", commit="0cfb5bbb8f079dff64c7bce1f11524b0e0c97a64")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq-epics-plugin/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v1_05_03"
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v1_05_04:"
    )
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("epics-base")

    depends_on("artdaq-utilities@:v1_99_00", when="@:v1_99_00")
    depends_on("artdaq-utilities@v2_00_00:,develop", when="@v2_00_00:,develop")
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
