# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPsycopg2(PythonPackage):
    """Python interface to PostgreSQL databases"""

    homepage = "https://psycopg.org/"
    pypi = "psycopg2/psycopg2-2.8.6.tar.gz"

    version(
        "2.9.13",
        sha256="d36784fc2dae69523ba4b79c7d1d1b4d6e83e87836874f111262f4db940b16a6",
    )
    version(
        "2.9.12",
        sha256="1dedb1c7a1d8552c4a6044c6b1c41a52e6a8e2d144af83eccac758076b1b7c15",
    )
    version(
        "2.9.11",
        sha256="964d31caf728e217c697ff77ea69c2ba0865fa41ec20bb00f0977e62fdcc52e3",
    )
    version(
        "2.9.10",
        sha256="12ec0b40b0273f95296233e8750441339298e6a572f7039da5b260e3c8b60e11",
    )
    version(
        "2.9.9",
        sha256="d1454bde93fb1e224166811694d600e746430c006fbb031ea06ecc2ea41bf156",
    )
    version(
        "2.9.8",
        sha256="3da6488042a53b50933244085f3f91803f1b7271f970f3e5536efa69314f6a49",
    )
    version(
        "2.9.7",
        sha256="f00cc35bd7119f1fed17b85bd1007855194dde2cbd8de01ab8ebb17487440ad8",
    )
    version(
        "2.9.6",
        sha256="f15158418fd826831b28585e2ab48ed8df2d0d98f502a2b4fe619e7d5ca29011",
    )
    version(
        "2.9.1",
        sha256="de5303a6f1d0a7a34b9d40e4d3bef684ccc44a49bbe3eb85e3c0bffb4a131b7c",
    )
    version(
        "2.8.6",
        sha256="fb23f6c71107c37fd667cb4ea363ddeb936b348bbd6449278eb92c189699f543",
    )

    depends_on("c", type="build")  # generated

    # https://www.psycopg.org/docs/install.html#prerequisites
    # https://github.com/psycopg/psycopg2/blob/master/doc/src/install.rst
    # https://www.psycopg.org/docs/news.html#news
    # https://pypi.org/project/psycopg2/#history
    depends_on("python@:3.11", when="@2.9.5:", type=("build", "link", "run"))
    depends_on("python@:3.10", when="@2.9.1:", type=("build", "link", "run"))
    depends_on("python@:3.9", when="@2.8.6:2.9.13", type=("build", "link", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("postgresql@9.1:18", when="@2.9.11:", type=("build", "link", "run"))
    depends_on("postgresql@9.1:17", when="@2.9.10", type=("build", "link", "run"))
    depends_on("postgresql@9.1:15", when="@2.9.4:2.9.9", type=("build", "link", "run"))
    depends_on("postgresql@9.1:14", when="@2.9.2:2.9.3", type=("build", "link", "run"))
    depends_on("postgresql@9.1:13", when="@2.9:2.9.1", type=("build", "link", "run"))
    depends_on("postgresql@9.1:12", when="@2.8.4:2.8", type=("build", "link", "run"))
    depends_on("postgresql@9.1:11", when="@2.8:2.8.3", type=("build", "link", "run"))
