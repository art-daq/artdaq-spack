# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys
from spack.util.environment import EnvironmentModifications
from llnl.util.filesystem import join_path

from spack.package import *

def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class Trace(CMakePackage):
    """TRACE is yet another logging (time stamp) tool, but it allows
    fast and/or slow logging - dynamically (you choose)."""

    homepage = "https://github.com/art-daq/trace"
    url = "https://github.com/art-daq/trace/archive/refs/tags/v3_17_07.tar.gz"
    git = "https://github.com/art-daq/trace.git"

    parallel = False

    depends_on("cetmodules@3.26.00:", type="build")

    version("develop", branch="develop", get_full_repo=True)
    version("v3_18_00", commit="30c44bc884375ad0aae6a45ab8940a8d9ce2091b")
    version("v3_17_17", commit="a7a6555ad7c0db31368e15a41e6ceb9f4e5312b6")
    version("v3_17_16", commit="c9a08f545867143d37b1c4d906b2164b95f940b5")
    version("v3_17_15", commit="716bee566b49c9edbceb1b0ae40562c2d0ec3648")
    version("v3_17_14", commit="4f0a54a354b7f19a7cc3874d2d7b48a24990a102")
    version("v3_17_13", commit="01865d3fc90e82f20b50da10b6a7993ab428bcf5")
    version("v3_17_12", commit="58433e1c560c4c6538c6f6fc79b04a106691749f")
    version("v3_17_11", commit="23f21ee9c53af5bd0e1b695038cda457517028fe")
    version("v3_17_10", commit="8f81c8f0fdbbb87e67d6cf9dd38ec13c5689d2a9")
    version("v3_17_09", commit="d93a64f45e57bec87c0b890b9bbaaf94eb0b2e69")
    version("v3_17_08", commit="791e287d62dd0d4dbf616cb30692f676e2dba8da")
    version("v3_17_07", commit="acd94af76d796e1edf963faa282e1389ebae9bbc")
    version("v3_17_06", commit="41736440d4be0f2adaa376bf8d230d4eccc540ce")
    version("v3_17_05", commit="2dfadcd237b1253426166a0a9f7c8ce250c3f27e")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/trace/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    depends_on("cxx", type="build")
    variant("kmod", default=False, description="Create Linux kernel module")
    variant("mf", default=False, description="Compile MessageFacility library")

    patch("stronger_want_kmod.patch", when="@:v3_17_13")

    depends_on("messagefacility", when="+mf")

    def cmake_args(self):
        args = ["-DWANT_KMOD={0}".format("TRUE" if "+kmod" in self.spec else "FALSE"),"-DWANT_MF={0}".format("TRUE" if "+mf" in self.spec else "FALSE")]
        return args

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # Perl modules.
        env.prepend_path("PERL5LIB", os.path.join(prefix, "perllib"))
        # Cleaup.
        sanitize_environments(env, "PATH", "CET_PLUGIN_PATH", "PERL5LIB")

    def setup_run_environment(self, env):
        prefix = self.prefix

        # Source the functions
        file_to_source = self.prefix.join("bin/trace_functions.sh")
        print(f'source {file_to_source}')

        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # Perl modules.
        env.prepend_path("PERL5LIB", os.path.join(prefix, "perllib"))
        # Cleaup.
        sanitize_environments(env, "PATH", "CET_PLUGIN_PATH", "PERL5LIB")

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # Perl modules.
        env.prepend_path("PERL5LIB", os.path.join(prefix, "perllib"))
        # Cleaup.
        sanitize_environments(env, "PATH", "CET_PLUGIN_PATH", "PERL5LIB")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix

        # Source the functions
        file_to_source = self.prefix.join("bin/trace_functions.sh")
        print(f'source {file_to_source}')

        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # Perl modules.
        env.prepend_path("PERL5LIB", os.path.join(prefix, "perllib"))
        # Cleaup.
        sanitize_environments(env, "PATH", "CET_PLUGIN_PATH", "PERL5LIB")
