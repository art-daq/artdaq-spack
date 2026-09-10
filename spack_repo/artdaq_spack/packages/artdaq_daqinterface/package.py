# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class ArtdaqDaqinterface(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq-daqinterface/archive/refs/tags/v3_12_02.tar.gz"
    git = "https://github.com/art-daq/artdaq-daqinterface.git"

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq-daqinterface/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    version("develop", branch="develop", get_full_repo=True)
    version("v4_08_00", commit="ced29821e2fcd871ce7286054339b2defae9cbb8")
    version("v4_07_00", commit="b3158940a1050aa5def28be6cff5ef9ab000af9c")
    version("v4_06_00", commit="0f0b1c93c75ac11cee5ec9a4f29ffcc32985d535")
    version("v4_05_00", commit="59b343817539170a62bf0a20280ef01cf7d242e2")
    version("v4_04_00", commit="406bc84ffcb3c2c7b749d7e4eeab065d4404fbf1")
    version("v4_03_01", commit="c5f510441c256c1b6f6b532dc8b7db7ed8609448")
    version("v4_03_00", commit="8e2c60f9546a8c209bdf444bd186653b865f226a")
    version("v4_02_00", commit="61c5a10803301fccb27bd0b03fc664cac7a757c6")
    version("v4_01_00", commit="0f0cc2e2f98551c1948c19afd542e8e875b3df6e")
    version("v4_00_00", commit="578923aa70322fcfc2906f85e9110d7ba573998e")
    version("v3_16_00", commit="b134b71dda67b747d071e694fc021c2d8461b1ce")
    version("v3_15_00", commit="ceb0f3c8c67b9f2042dbff8d3a804fad91bfab90")
    version("v3_14_01", commit="98c6cc84ad5e213dc81b8bd6f1be36222dc103f0")
    version("v3_14_00", commit="a8218c8422f5e9eaa326e9ff8a84ad0e0585b6b7")
    version("v3_13_01", commit="45975dd99120a1b07c8501ee8e79ad2ea1e7ab23")
    version("v3_13_00", commit="fa5536491b37c46a6c19f2fae43d74bdaf04f5e3")
    version("v3_12_07", commit="60c0a2c53f42bd6e9e31310477a20ac73807415d")
    version("v3_12_05", commit="9a95f152af24783d13380f840e0f9b4ef16cab20")
    version("v3_12_04", commit="bedb67048b1ff7b6f3ed59510460574e8e550ca8")
    version("v3_12_03", commit="cd909f5c12191d63f2894287a67a2fd8c5854945")
    version("v3_12_02", commit="d3f787e238ab5c17a84a14465aa997e3eb3f4268")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("db", default=False, description="Enable database support")

    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("python@3:")
    depends_on("py-psycopg2", when="+db")

    def setup_run_environment(self, env):
        prefix = self.prefix
        env.set("ARTDAQ_DAQINTERFACE_DIR", prefix)
        env.set("ARTDAQ_DAQINTERFACE_VERSION", "SPACK")  # Needed by source_me

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        env.set("ARTDAQ_DAQINTERFACE_DIR", prefix)
        env.set("ARTDAQ_DAQINTERFACE_VERSION", "SPACK")  # Needed by source_me
