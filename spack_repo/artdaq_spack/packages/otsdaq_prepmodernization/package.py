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



class OtsdaqPrepmodernization(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq-prepmodernization/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq-prepmodernization.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v3_00_00", commit="e66ae40b1a7d03887681b8465a9eb57e91ec1ae4")
    version("v2_10_00", commit="40f6197b16c5e1f040a9638c572da383771a929a")
    version("v2_09_01", commit="73339975d4130bbe5e97ffbb83342e07e56d498f")
    version("v2_09_00", commit="b238f2e3feeab28fadf47d8cc40267363a5bd9b0")
    version("v2_08_02", commit="637dcff1fbdafcd775e12eea2384202ff84dd3d9")
    version("v2_08_01", commit="f4a12f00d6f7709bdcfddcad49c9ee38f0cc69e3")
    version("v2_08_00", commit="c28c948dc934dd6370c5919c6c68e3bdb9d8feba")
    version("v2_07_00", commit="0966c03205416c41913b4e23aef21b417e48099e")
    version("v2_06_11", commit="82a680ad2adde195f9c80ed112278c24801f7c98")
    version("v2_06_10", commit="50748b05521346bd8cf8ab5c70f3711760fbb44c")
    version("v2_06_09", commit="9ac1821a9b432dd366ee404c4a5929783934dec1")
    version("v2_06_08", commit="70d400ec9d03cea9ec60429954b845d667c88622")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq-prepmodernization/archive/refs/tags/{0}.tar.gz"
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
    depends_on("c", type="build")
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
