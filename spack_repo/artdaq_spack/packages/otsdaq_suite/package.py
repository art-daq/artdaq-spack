# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from sys import version

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *

class OtsdaqSuite(BundlePackage):
    """The Off-The-Shelf DAQ suite, otsdaq, providing graphical wrappers for artdaq
    """

    version("develop")
    version("v3_05_00")
    version("v3_04_02")
    version("v3_04_01")
    version("v3_04_00")
    version("v3_03_01")
    version("v3_03_00")
    version("v3_02_00")
    version("v3_01_00")
    version("v3_00_00")
    version("v2_10_00")
    version("v2_09_01")
    version("v2_09_00")
    version("v2_08_02")
    version("v2_08_01")
    version("v2_08_00")
    version("v2_07_00")
    version("v2_06_11")
    version("v2_06_10")
    version("v2_06_09")
    version("v2_06_08")

    squals = ("112", "117", "118", "120", "120a", "120b", "122", "123", "124", "126", "128", "130", "131", "132", "133")
    variant(
        "s",
        default="133",
        values=("0",) + squals,
        multi=False,
        description="Art suite version to use",
    )
    for squal in squals:
        depends_on(f"art-suite@s{squal}+root+bundle", when=f"s={squal}")
    depends_on(f"art-suite+root", when="s=0")

    variant(
        "artdaq",
        default="31600",
        values = ("0","31202","31203","31204", "31205", "31207", "31300", "31301", "31400", "31401", "31500", "31600"),
        multi=False,
        description="Artdaq suite version to use",
        when="@:v3_00_00"
    )
    variant(
        "artdaq",
        default="40500",
        values = ("0","40000","40100","40200", "40300", "40301", "40400", "40401", "40500"),
        multi=False,
        description="Artdaq suite version to use",
        when="@v3_00_00:"
    )

    depends_on("artdaq-suite@v4_05_00", when="artdaq=40500")
    depends_on("artdaq-suite@v4_04_01", when="artdaq=40401")
    depends_on("artdaq-suite@v4_04_00", when="artdaq=40400")
    depends_on("artdaq-suite@v4_03_01", when="artdaq=40301")
    depends_on("artdaq-suite@v4_03_00", when="artdaq=40300")
    depends_on("artdaq-suite@v4_02_00", when="artdaq=40200")
    depends_on("artdaq-suite@v4_01_00", when="artdaq=40100")
    depends_on("artdaq-suite@v4_00_00", when="artdaq=40000")
    depends_on("artdaq-suite@v3_16_00", when="artdaq=31600")
    depends_on("artdaq-suite@v3_15_00", when="artdaq=31500")
    depends_on("artdaq-suite@v3_14_01", when="artdaq=31401")
    depends_on("artdaq-suite@v3_14_00", when="artdaq=31400")
    depends_on("artdaq-suite@v3_13_01", when="artdaq=31301")
    depends_on("artdaq-suite@v3_13_00", when="artdaq=31300")
    depends_on("artdaq-suite@v3_12_07", when="artdaq=31207")
    depends_on("artdaq-suite@v3_12_05", when="artdaq=31205")
    depends_on("artdaq-suite@v3_12_04", when="artdaq=31204")
    depends_on("artdaq-suite@v3_12_03", when="artdaq=31203")
    depends_on("artdaq-suite@v3_12_02", when="artdaq=31202")
    depends_on("artdaq-suite+db+epics")

    variant("demo", default=False, description="Install otsdaq-demo")
    variant("prep", default=False, description="Install PREP modernization library")

    variant("ci", default=True, description="Install utilities used by CI builds")
    with when("+ci"):
        depends_on("lcov")
        depends_on("py-black")
        depends_on("py-cmake-format")

    with when("@develop"):
        depends_on("otsdaq")
        depends_on("otsdaq-utilities")
        depends_on("otsdaq-components")
        depends_on("otsdaq-epics")
        depends_on("otsdaq-demo", when="+demo")
        depends_on("otsdaq-prepmodernization", when="+prep")

        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx")
        depends_on("xdaq")
        depends_on("reredirect")
    with when("@v3_05_00"):
        depends_on("otsdaq@v3_05_00")
        depends_on("otsdaq-utilities@v3_04_00")
        depends_on("otsdaq-components@v3_03_00")
        depends_on("otsdaq-epics@v3_03_00")
        depends_on("otsdaq-demo@v3_05_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_02_00", when="+prep")
        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v3_04_02"):
        depends_on("otsdaq@v3_04_02")
        depends_on("otsdaq-utilities@v3_03_02")
        depends_on("otsdaq-components@v3_02_00")
        depends_on("otsdaq-epics@v3_02_00")
        depends_on("otsdaq-demo@v3_04_01", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_01_00", when="+prep")
        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v3_04_01"):
        depends_on("otsdaq@v3_04_01")
        depends_on("otsdaq-utilities@v3_03_01")
        depends_on("otsdaq-components@v3_02_00")
        depends_on("otsdaq-epics@v3_02_00")
        depends_on("otsdaq-demo@v3_04_01", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_01_00", when="+prep")
        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v3_04_00"):
        depends_on("otsdaq@v3_04_00")
        depends_on("otsdaq-utilities@v3_03_00")
        depends_on("otsdaq-components@v3_02_00")
        depends_on("otsdaq-epics@v3_02_00")
        depends_on("otsdaq-demo@v3_04_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_01_00", when="+prep")
        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v3_03_01"):
        depends_on("otsdaq@v3_03_00")
        depends_on("otsdaq-utilities@v3_02_00")
        depends_on("otsdaq-components@v3_01_00")
        depends_on("otsdaq-epics@v3_01_00")
        depends_on("otsdaq-demo@v3_03_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_00_00", when="+prep")
        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v3_03_00"):
        depends_on("otsdaq@v3_03_00")
        depends_on("otsdaq-utilities@v3_02_00")
        depends_on("otsdaq-components@v3_01_00")
        depends_on("otsdaq-epics@v3_01_00")
        depends_on("otsdaq-demo@v3_03_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_00_00", when="+prep")
        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v3_02_00"):
        depends_on("otsdaq@v3_02_00")
        depends_on("otsdaq-utilities@v3_01_00")
        depends_on("otsdaq-components@v3_00_00")
        depends_on("otsdaq-epics@v3_00_00")
        depends_on("otsdaq-demo@v3_02_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_00_00", when="+prep")
        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v3_01_00"):
        depends_on("otsdaq@v3_01_00")
        depends_on("otsdaq-utilities@v3_00_00")
        depends_on("otsdaq-components@v3_00_00")
        depends_on("otsdaq-epics@v3_00_00")
        depends_on("otsdaq-demo@v3_01_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_00_00", when="+prep")

        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v3_00_00"):
        depends_on("otsdaq@v3_00_00")
        depends_on("otsdaq-utilities@v3_00_00")
        depends_on("otsdaq-components@v3_00_00")
        depends_on("otsdaq-epics@v3_00_00")
        depends_on("otsdaq-demo@v3_00_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v3_00_00", when="+prep")

        # External Dependencies not in art-suite or artdaq-suite
        depends_on("libpqxx@7.10.0")
        depends_on("xdaq@16_35_0_4")
        depends_on("reredirect@0.3")
    with when("@v2_10_00"):
        depends_on("otsdaq@v2_10_00")
        depends_on("otsdaq-utilities@v2_10_00")
        depends_on("otsdaq-components@v2_10_00")
        depends_on("otsdaq-epics@v2_10_00")
        depends_on("otsdaq-demo@v2_10_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_10_00", when="+prep")
    with when("@v2_09_01"):
        depends_on("otsdaq@v2_09_01")
        depends_on("otsdaq-utilities@v2_09_01")
        depends_on("otsdaq-components@v2_09_01")
        depends_on("otsdaq-epics@v2_09_01")
        depends_on("otsdaq-demo@v2_09_01", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_09_01", when="+prep")
    with when("@v2_09_00"):
        depends_on("otsdaq@v2_09_00")
        depends_on("otsdaq-utilities@v2_09_00")
        depends_on("otsdaq-components@v2_09_00")
        depends_on("otsdaq-epics@v2_09_00")
        depends_on("otsdaq-demo@v2_09_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_09_00", when="+prep")
    with when("@v2_08_02"):
        depends_on("otsdaq@v2_08_02")
        depends_on("otsdaq-utilities@v2_08_02")
        depends_on("otsdaq-components@v2_08_02")
        depends_on("otsdaq-epics@v2_08_02")
        depends_on("otsdaq-demo@v2_08_02", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_08_02", when="+prep")
    with when("@v2_08_01"):
        depends_on("otsdaq@v2_08_01")
        depends_on("otsdaq-utilities@v2_08_01")
        depends_on("otsdaq-components@v2_08_01")
        depends_on("otsdaq-epics@v2_08_01")
        depends_on("otsdaq-demo@v2_08_01", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_08_01", when="+prep")
    with when("@v2_08_00"):
        depends_on("otsdaq@v2_08_00")
        depends_on("otsdaq-utilities@v2_08_00")
        depends_on("otsdaq-components@v2_08_00")
        depends_on("otsdaq-epics@v2_08_00")
        depends_on("otsdaq-demo@v2_08_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_08_00", when="+prep")
    with when("@v2_07_00"):
        depends_on("otsdaq@v2_07_00")
        depends_on("otsdaq-utilities@v2_07_00")
        depends_on("otsdaq-components@v2_07_00")
        depends_on("otsdaq-epics@v2_07_00")
        depends_on("otsdaq-demo@v2_07_00", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_07_00", when="+prep")
    with when("@v2_06_11"):
        depends_on("otsdaq@v2_06_11")
        depends_on("otsdaq-utilities@v2_06_11")
        depends_on("otsdaq-components@v2_06_11")
        depends_on("otsdaq-epics@v2_06_11")
        depends_on("otsdaq-demo@v2_06_11", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_06_11", when="+prep")
    with when("@v2_06_10"):
        depends_on("otsdaq@v2_06_10")
        depends_on("otsdaq-utilities@v2_06_10")
        depends_on("otsdaq-components@v2_06_10")
        depends_on("otsdaq-epics@v2_06_10")
        depends_on("otsdaq-demo@v2_06_10", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_06_10", when="+prep")
    with when("@v2_06_09"):
        depends_on("otsdaq@v2_06_09")
        depends_on("otsdaq-utilities@v2_06_09")
        depends_on("otsdaq-components@v2_06_09")
        depends_on("otsdaq-epics@v2_06_09")
        depends_on("otsdaq-demo@v2_06_09", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_06_09", when="+prep")
    with when("@v2_06_08"):
        depends_on("otsdaq@v2_06_08")
        depends_on("otsdaq-utilities@v2_06_08")
        depends_on("otsdaq-components@v2_06_08")
        depends_on("otsdaq-epics@v2_06_08")
        depends_on("otsdaq-demo@v2_06_08", when="+demo")
        depends_on("otsdaq-prepmodernization@v2_06_08", when="+prep")
