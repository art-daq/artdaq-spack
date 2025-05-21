# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class OtsdaqEpics(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq-epics/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq-epics.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v3_00_00", commit="350e5a92d99636a5a866a3fd9b7128114e1ca9a6")
    version("v2_10_00", commit="245f56ddb5345c8199c5bb8c765ee1b0ba727620")
    version("v2_09_01", commit="2312d9c1fb7dce852e36aab59d8735d4626193d8")
    version("v2_09_00", commit="966d63a39d3c61b59a5909ce2c0747e8ef69eec3")
    version("v2_08_02", commit="77c961a8be6114f0a374fabef458558ed849b72f")
    version("v2_08_01", commit="01ce6cddcc7be28e79c86893b99c114cb12b142f")
    version("v2_08_00", commit="33cfc3b3dfc47e175fd0b72e42eaef56c2746828")
    version("v2_07_00", commit="d5651b1e27be1418d66a815c9d6dfe06613642eb")
    version("v2_06_11", commit="6214e687c895ddb1e30b8bf14ab89801c5f4cb31")
    version("v2_06_10", commit="7e2f91eb7c161e21900526b0440fc765d005b720")
    version("v2_06_09", commit="586ee271a7c301b1a0efddb59b6ba008280651d0")
    version("v2_06_08", commit="32bdbcd6ec727eda64766aa2d70ae2b7871a98eb")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq-epics/archive/refs/tags/{0}.tar.gz"
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
    depends_on("epics-base")
    depends_on("libpqxx")

    depends_on("otsdaq@:v2_99_00", when="@:v2_99_00")
    depends_on("otsdaq@v3_00_00:,develop", when="@v3_00_00:,develop")
    depends_on("otsdaq-utilities@:v2_99_00", when="@:v2_99_00")
    depends_on("otsdaq-utilities@v3_00_00:,develop", when="@v3_00_00:,develop")
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
