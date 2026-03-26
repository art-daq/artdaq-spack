# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class OtsdaqComponents(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = (
        "https://github.com/art-daq/otsdaq-components/archive/refs/tags/v2_06_08.tar.gz"
    )
    git = "https://github.com/art-daq/otsdaq-components.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v3_04_00", commit="ec63478f68c8a90d688ceb95a7ffe10dafaa7288")
    version("v3_03_01", commit="eb5e2463f182149c7783eb04bb2e2f31801d2f70")
    version("v3_03_00", commit="2989fc5cb48b38339801c0cfc480021cd535b24f")
    version("v3_02_00", commit="aef647cbdd7de3983dda111b868ec0df2164d655")
    version("v3_01_00", commit="c893949ef91cd5ddade0c9ac2c2da73fd2116226")
    version("v3_00_00", commit="c649716a54930da35e58b4e37017093d031304ee")
    version("v2_10_00", commit="1938539dbdc9c6af78d3557093bcaffcf7e8f666")
    version("v2_09_01", commit="e6d2288c0003a1d229d5e01f858da13c79f72b75")
    version("v2_09_00", commit="df7919878c5407b70909da47c300a24a495ef2e6")
    version("v2_08_02", commit="3b4c2043bee1409df8922b900e5e07e6358c842a")
    version("v2_08_01", commit="3be5282e5ed9d525c36df3ca5967e5942b09077c")
    version("v2_08_00", commit="75945ea1fc9f363e2a01bfb61d31c599d880069d")
    version("v2_07_00", commit="7f4eda5db28ee192b23584f50d0b2fec566c0f4a")
    version("v2_06_11", commit="a0dfcfc74618db231ad548fc463f5cb1608bd940")
    version("v2_06_10", commit="d496c91315157b5a5e531b2f89856b978b82949e")
    version("v2_06_09", commit="368b6a3413681ade8c62581c9751ba18ffa1f159")
    version("v2_06_08", commit="75a30ad1bfb44b0817e791a9cea993df8cc33c7c")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaqcomponents/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v2_06_09",
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v2_06_10:",
    )
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules@3.26.00:", type="build")

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
