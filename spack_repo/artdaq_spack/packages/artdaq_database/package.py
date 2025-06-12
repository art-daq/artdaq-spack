# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class ArtdaqDatabase(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq-database/archive/refs/tags/v1_07_02.tar.gz"
    git = "https://github.com/art-daq/artdaq-database.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_00_00", commit="866afa9b6518136994fba5425bc3d819ee118940")
    version("v1_10_02", commit="2e92a4357c9b4a7dbe2259a8d6dcf9b1dc39d582")
    version("v1_10_01", commit="43e8e3a4f0327f0bb6c381b75037eb51fa5719fd")
    version("v1_10_00", commit="9d80e35a2052c04a92cddd2691d760aa280811eb")
    version("v1_09_00", commit="06041b749dd2b6fde936f54d34d179f99eed1229")
    version("v1_07_04", commit="e382aa88f23d70409508a3cbeae378ddb83cec1f")
    version("v1_07_03", commit="2cb8098b33333f92c96273d8bb959657e7eb3c25")
    version("v1_07_02", commit="a3d27b761786aeb7fdff6dc1baeaca9b8bedbcce")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq-database/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v1_07_03"
    )
    variant(
        "cxxstd",
        default="20",
        values=("17","20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v1_07_04:"
    )
    variant("builtin_fhicl", default=True, description="Use built-in FHiCL-cpp with database fixes")

    depends_on("curl")
    depends_on("boost+filesystem+program_options")
    depends_on("swig", type="build")
    depends_on("node-js", type="build", when="@:v1_07_05")
    depends_on("python", type="build")
    depends_on("art-suite")

    depends_on("cetmodules@3.26.00:", type="build")

    depends_on("cetlib", when="~builtin_fhicl")

    depends_on("trace+mf")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
                "-DUSE_FHICLCPP={0}".format("TRUE" if "+builtin_fhicl" in self.spec else "FALSE")]
        return args
