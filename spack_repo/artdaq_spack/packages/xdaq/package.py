# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from re import A
import sys

from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack.package import *

def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Xdaq(MakefilePackage):
    """Programming library for writing an XML-RPC server or client in
    C or C++."""

    homepage = "https://gitlab.cern.ch/cmsos/core"
    url = "https://gitlab.cern.ch/cmsos/core/-/archive/release_16_21_0_2/core-release_16_21_0_2.tar.gz"
    git = "https://gitlab.cern.ch/cmsos/core.git"

    version("16_35_0_4", sha256="e1480b2ec98585b422595e8b6f9babbcc80638de2fb56e3e751929ab14283d53")
    version("16_34_0_4", sha256="ae12bd8d69443e20961ded7838175a097950c430fd76f514583b0c5724a17064")
    version("16_33_0_4", sha256="ed41d8fe0943e8ef0651de7fac1f9e8efab5c1710a73779276ba09aa7b208021")
    version("16_32_0_4", sha256="e95eb6aa5b3f348a3af8b6844a83ec26a386efc02a008ded9b71cc56c98d47db")
    version("16_31_0_4", sha256="a3a9bb0a0194795b8141e32fc02ad9dedb7d572e3b82e3d909bf2380c652fcde")
    version("16_30_0_4", sha256="6a2659357e59e6d5ebb37616efed33d86d4bb8eafe9a057ebda88dc4f65dec7d")
    version("16_29_0_3", sha256="e9100300c08fcc186b060d6f07498466245e51db0f9b61b84f00bc9472bf284a")
    version("16_28_0_3", sha256="68b11e89085d3c6abf482a1df257d3a5e29828d23d8bd4f8afdfc55daf096fe9")
    version("16_27_0_3", sha256="fbfb5a7d3b71ce9920304856036dbd71537ef17f7ea67cda8713ab64e54681df")
    version("16_26_0_3", sha256="cd425bfde654f108f6634b1a8f7f2af8549fd2386b8ea5f0e47d3d8042c9519e")
    version("16_25_0_2", sha256="576dc4dbc84a876eea786bfd502a9d085d0cc02dd6981b20e15f631982a3a232")
    version("16_24_0_2", sha256="15ad2237b754e76890dded6f1c760b6d2a0c6936a55345c6a7cd1ed1011e7f57")
    version("16_23_0_2", sha256="38023cd80a1fe587b294819902b9efdf0b2501cf1cda02ff91bcff69cbc442d7")
    version("16_21_0_2", sha256="e297be15f5541b1869a3c8e59cc3f7d12bd237269c9d88657e099da1a99b7cf7")
    version("15_29_0_3", sha256="fefc94045c32b2f04de12d94fcaf7a61106429c9c8fc69372b1e70609b4c1127")
    version("15_28_0_3", sha256="2129a42e490a7016b0970ad90f035b32368ac9798501265268a35fd48aa16d4d")
    version("15_27_0_3", sha256="8791a7afb9271b8ed00f6efdee21c2ae798dd43a3288d02c5a49e6bedeee3229")
    version("15_26_0_3", sha256="98fc2207a979c79458a4dbf2159f5c5b60201e8a7c46d2462051411859325c87")
    version("15_25_0_3", sha256="dfa1696406bdc1adc2949c35423661ba3507b1978397395b313ce345186bdcdd")
    version("15_24_0_3", sha256="18221218889832cdf50d267e986e541e7ba499915d6e2d521691135240976b70")
    version("15_23_0_3", sha256="6a17a0b7a58e6fc3c82bd83006fefca34e3aee8b275ff45948e2c6905fd6def4")

    conflicts("%gcc@13.1.0", when="@:16_31_0_3")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("numactl")
    depends_on("libtirpc")
    depends_on("libelf")
    depends_on("uuid")

    patch("mfDefs.core.patch")
    patch("build.Makefile.rules.patch")
    patch("build.mfDefs.linux.patch")
    patch("build.mfDefs.linux.2.patch")
    patch("extern.asyncresolv.configure.patch.patch")
    patch("extern.i2o.Makefile.patch")
    patch("extern.log4cplus.Makefile.patch")
    patch("extern.mimetic.patch")
    patch("extern.xalan.Makefile.patch")
    patch("toolbox.includes.patch")
    patch("toolbox.Makefile.patch")
    patch("toolbox.src.GNUC.patch")
    patch("xoap.filter.src.common.patch")

    depends_on("xerces-c@3.2")
    depends_on("nlohmann-json")
    depends_on("log4cplus")
    depends_on("xalan-c")
    depends_on("jansson")
    depends_on("c-ares")

    def patch(self):
        tirpc_include_dir = self.spec["libtirpc"].prefix.include.tirpc
        #print("TIRPC Include path: " + tirpc_include_dir)
        for dirpath, dirnames, filenames in os.walk("."):
            for filename in filenames:
                if "Makefile" in filename:
                    filepath = os.path.join(dirpath, filename)
                    filter_file("/usr/include/tirpc", tirpc_include_dir, filepath)


    def build(self, spec, prefix):
        # Removed "extern/nlohmannjson", "extern/log4cplus", "extern/jansson", "extern/xerces", "extern/xalan"
        externPackages=["extern/asyncresolv", "extern/i2o", "extern/cgicc", "extern/mimetic"]

        Packages=["config", "xcept", "log/udpappender", "log/xmlappender", "toolbox",
 "xoap", "xoap/filter", "xdata", "pt", "xgi", "i2o", "xdaq", "i2o/utils", "pt/http",
"pt/fifo", "executive", "hyperdaq", "xrelay", "b2in/nub", "b2in/utils", "b2in/eventing"]

        for extpackage in externPackages:
            make("Packages=" + extpackage, "CC="+env['CC'], "CXX="+env['CXX'], "install")
        for package in Packages:
            make("Packages="+package, "CC="+env['CC'], "CXX="+env['CXX'], "LD="+env['CXX'])
            make("-C" + package, "CC="+env['CC'], "CXX="+env['CXX'], "LD="+env['CXX'], "install")

    def install(self, spec, prefix):
        install_tree("./x86_64_slc6", prefix)
        install_tree("./x86_64_slc6/include/linux", os.path.join(prefix,"include"))

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))

        # XDAQ Variables
        env.set("XDAQ_ROOT", prefix)
        env.set("XDAQ_DOCUMENT_ROOT", os.path.join(prefix, "htdocs"))
        env.set("XDAQ_OS", "linux")
        env.set("XDAQ_PLATFORM", "x86_64_slc6")
        env.set("XDAQ_SETUP_ROOT", os.path.join(prefix, "share"))
        env.set("BUILD_HOME", prefix)
        env.set("PROJECT_NAME", "core")
        env.set("BUILD_SUPPORT", "build")


        # Cleaup.
        sanitize_environments(env, "PATH")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))

        # XDAQ Variables
        env.set("XDAQ_ROOT", prefix)
        env.set("XDAQ_DOCUMENT_ROOT", os.path.join(prefix, "htdocs"))
        env.set("XDAQ_OS", "linux")
        env.set("XDAQ_PLATFORM", "x86_64_slc6")
        env.set("XDAQ_SETUP_ROOT", os.path.join(prefix, "share"))

        # Cleaup.
        sanitize_environments(env, "PATH")

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))

        # XDAQ Variables
        env.set("XDAQ_ROOT", prefix)
        env.set("XDAQ_DOCUMENT_ROOT", os.path.join(prefix, "htdocs"))
        env.set("XDAQ_OS", "linux")
        env.set("XDAQ_PLATFORM", "x86_64_slc6")
        env.set("XDAQ_SETUP_ROOT", os.path.join(prefix, "share"))
        env.set("BUILD_HOME", prefix)
        env.set("PROJECT_NAME", "core")
        env.set("BUILD_SUPPORT", "build")

        # Cleaup.
        sanitize_environments(env, "PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))

        # XDAQ Variables
        env.set("XDAQ_ROOT", prefix)
        env.set("XDAQ_DOCUMENT_ROOT", os.path.join(prefix, "htdocs"))
        env.set("XDAQ_OS", "linux")
        env.set("XDAQ_PLATFORM", "x86_64_slc6")
        env.set("XDAQ_SETUP_ROOT", os.path.join(prefix, "share"))

        # Cleaup.
        sanitize_environments(env, "PATH")
