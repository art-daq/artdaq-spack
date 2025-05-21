# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class ArtdaqMfextensions(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq-mfextensions/archive/refs/tags/v1_08_02.tar.gz"
    git = "https://github.com/art-daq/artdaq-mfextensions.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_00_00", commit="045291d136374fe9a064001a76e6781df2491ac7")
    version("v1_10_00", commit="6be6276c9c7798ab032935ca8053f910dd65b116")
    version("v1_09_02", commit="15e8f5c4c57e21039adfe956bf456627699f1c66")
    version("v1_09_01", commit="67df43b925235736cef91497e3148325e96b4ee6")
    version("v1_09_00", commit="f27e0c459f0b7678abe1003d9fdf3653a6b9385b")
    version("v1_08_06", commit="ab071ccb57173931f30130aa33b52a48e9d28d7c")
    version("v1_08_05", commit="153289123420aea7dee0bea0e560055db651aa07")
    version("v1_08_04", commit="458481dadefd5b8ebf9ec1e318f0853e9160bdf3")
    version("v1_08_03", commit="8e83c0cb8c5d8c8d8fa5fd2b268c5afbb23d4ea4")
    version("v1_08_02", commit="e8bee6a61cdbfadea9c96c95865dc138c2bdf815")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq-mfextensions/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v1_08_03"
    )
    variant(
        "cxxstd",
        default="20",
        values=( "17","20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v1_08_04:"
    )
    depends_on("cxx", type="build")

    variant("kafka", default=True, description="Build the Kafka destination, which depends on librdkafka")
    variant("curl", default=True, description="Build the SMTP destination, which depends on libcurl")

    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("qt@5.15:")
    depends_on("librdkafka", when="+kafka")
    depends_on("curl", when="+curl")

    depends_on("trace+mf")
    depends_on("art-suite")

    with when('@:v1_08_07'):
        def cmake_args(self):
            args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"), self.define('IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES', True) ]
            return args

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
