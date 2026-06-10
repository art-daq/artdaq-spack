# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

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
    version("v3_03_01", commit="da51e1ea3713d0cb62c0225d8330a9b4bf1441f9")
    version("v3_03_00", commit="eae8e23e1eae3951e730e5e98fe4bbf87884e673")
    version("v3_02_00", commit="b75023c0fc2e17985dbd3bbab408f015a3f314cb")
    version("v3_01_00", commit="b3ac069989719b098fdc0bdfabf5bee047a72995")
    version("v3_00_00", commit="43c21bc9c3b6abc3a4d2a3ce8aaa71ff655b9e5c")
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
        when="@:v1_07_03",
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v1_07_04:",
    )

    depends_on("curl")
    depends_on("boost+filesystem+program_options")
    depends_on("swig", type="build")
    depends_on("node-js", type="build", when="@:v1_07_05")
    depends_on("python", type="build")
    depends_on("art-suite")
    depends_on("fhicl-cpp+db")

    depends_on("mongo-cxx-driver+dots_in_keys", type="build")
    depends_on("cetmodules@3.26.00:", type="build")

    depends_on("cetlib", when="~builtin_fhicl")

    depends_on("trace+mf")

    variant("builtin_fhicl", default=False)

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args
