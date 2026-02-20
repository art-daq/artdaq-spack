# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack.package import *


class Reredirect(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/jerome-pouiller/reredirect/"
    url = "https://github.com/jerome-pouiller/reredirect/archive/refs/tags/v0.3.tar.gz"

    license("mit", checked_by="eflumerf")

    version(
        "0.3", sha256="ec01398ee442ff1223bcad608811b8cae2d116a1e519e2dc40fe48a4a6220e91"
    )

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("PREFIX=.*", "PREFIX=" + prefix)
        pass
