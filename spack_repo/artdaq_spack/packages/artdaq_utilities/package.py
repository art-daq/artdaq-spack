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


class ArtdaqUtilities(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = (
        "https://github.com/art-daq/artdaq-utilities/archive/refs/tags/v1_08_02.tar.gz"
    )
    git = "https://github.com/art-daq/artdaq-utilities.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_04_00", commit="06749c5984c85f02dfc249c3b854d6dbee02a807")
    version("v2_03_00", commit="9d0565de39b6c93fbb6468ccea58dde18f6c0e08")
    version("v2_02_00", commit="8b0c8dfc2310c742e5033c64070aeeeea3e62e08")
    version("v2_01_01", commit="bf46ab824d84f962ef486427874ee4c4cb2615a2")
    version("v2_01_00", commit="9c62249488feedb5f39345766d1b25acc871d55a")
    version("v2_00_00", commit="c564141ac7d5bbb2178714acfb9b085ea1c5a2de")
    version("v1_11_00", commit="62e841ecc45baeccfaf49ceafc3151f7f75c4b97")
    version("v1_10_00", commit="096107fb46013bb4f402b27e885f7d37384b186a")
    version("v1_09_01", commit="08a117ded7ea08f938af06f0e3091ac701f4ec2b")
    version("v1_09_00", commit="dd5eea2969fa2bbe31867355a43a9d0fa48c95cd")
    version("v1_08_06", commit="af854ea523eb836179e6ceef4ffb4f59b3084085")
    version("v1_08_04", commit="9690361a4b7f03aaf34e7c7add6aa77cb8a2c1f6")
    version("v1_08_03", commit="8cd890a2f46901100975e19a88ebddb1b3e302ff")
    version("v1_08_02", commit="c3382790c56b109adeae0eaf30a5a9f422d6ccbf")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq-utilities/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v1_08_03",
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v1_08_04:",
    )
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("messagefacility")
    depends_on("art-suite")

    depends_on("trace+mf")

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
