# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from distutils.util import check_environ

from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Artdaq(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq/archive/refs/tags/v3_12_04.tar.gz"
    git = "https://github.com/art-daq/artdaq.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v4_09_00", commit="72f74ad95420fa5b6014a873ebb1dab4265f9729")
    version("v4_08_00", commit="c7ff524d3d2f2f92fe0a1c3d8d7e121f96346762")
    version("v4_07_00", commit="0abc35d95466960fa4792b6bd591dc7e7acb128d")
    version("v4_06_00", commit="3bb38cb25f8d37cb235ee683c169a502ac1cd78a")
    version("v4_05_00", commit="3dc9f1d8a414cf8a0f0268d7a47d74963671e40c")
    version("v4_04_01", commit="b17c846d9ca5d6f5711e44f35da4853e2e8baa01")
    version("v4_04_00", commit="76516eed02e96efc819c676a3dd1e5fa38467be3")
    version("v4_03_00", commit="bb2530447184e036f652dd3c2806deec46b777b6")
    version("v4_02_00", commit="113c6d8cf0756933ed6084dcfa39eb02cdaa6072")
    version("v4_01_00", commit="0ef207134e76906c77269ac24f573bd904e604c3")
    version("v4_00_00", commit="cc48fb09d08cef36958832829a54578badb4a2b1")
    version("v3_16_00", commit="920cdfabcde642b66698d79ed74998cdf36c0bb1")
    version("v3_15_00", commit="3f67f5216e183e0701e14db4b2e7a45877579a9d")
    version("v3_14_01", commit="1d6e7037dd85c31525f863e035f0b423367d637b")
    version("v3_14_00", commit="2006c00ed3c2480ecbea6e18fb8f5711df7529c2")
    version("v3_13_01", commit="4eb46d5bd3b4f00973f99114efe66428c6f44626")
    version("v3_13_00", commit="0317da6544fbda80a760f2cac264bc6d1a328fc7")
    version("v3_12_07", commit="8dd14f2717a3bf0599cf97b71df2f15f048134c8")
    version("v3_12_05", commit="cf2f521077a6c2f1f34305352041d16647407798")
    version("v3_12_04", commit="00490715245ee5a51d4ac1ea5a48cd0b8545dc32")
    version("v3_12_03", commit="263fc0a133e64023bf830aa951f961359eb814a4")
    version("v3_12_02", commit="81c48f5aa55b9f5f821ebc19d84bbd8c0f834aaf")
    version("v3_12_01", commit="6239d41e5cea107b918897524fd7714cf00cd424")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v3_12_03",
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v3_12_04:",
    )

    depends_on("art-root-io cxxstd=17", when="cxxstd=17")
    depends_on("art-root-io cxxstd=20", when="cxxstd=20")

    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("xmlrpc-c+curl")
    depends_on("swig", type="build")
    depends_on("node-js", type="build", when="@:v3_12_06")

    depends_on("artdaq-core@:v3_99_00", when="@:v3_99_00")
    depends_on("artdaq-core@v4_00_00:,develop", when="@v4_00_00:,develop")
    depends_on("artdaq-utilities@:v1_99_00", when="@:v3_99_00")
    depends_on("artdaq-utilities@v2_00_00:,develop", when="@v4_00_00:,develop")
    depends_on("artdaq-mfextensions@:v1_99_00", when="@:v3_99_00")
    depends_on("artdaq-mfextensions@v2_00_00:,develop", when="@v4_00_00:,develop")
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
