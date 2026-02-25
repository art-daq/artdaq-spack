# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySlackSdk(PythonPackage):
    """The Slack platform offers several APIs to build apps.
    Each Slack API delivers part of the capabilities from the platform,
    so that you can pick just those that fit for your needs.
    This SDK offers a corresponding package for each of Slack’s APIs.
    They are small and powerful when used independently, and work seamlessly when used together, too.
    """

    homepage = "https://github.com/slackapi/python-slack-sdk"
    pypi = "slack_sdk/slack_sdk-3.40.1.tar.gz"

    license("MIT", checked_by="eflumerf")

    version(
        "3.40.1",
        sha256="a215333bc251bc90abf5f5110899497bf61a3b5184b6d9ee35d73ebf09ec3fd0",
    )
    version(
        "3.40.0",
        sha256="87b9a79d1d6e19a2b1877727a0ec6f016d82d30a6a410389fba87c221c99f10e",
    )
    version(
        "3.39.0",
        sha256="6a56be10dc155c436ff658c6b776e1c082e29eae6a771fccf8b0a235822bbcb1",
    )
    version(
        "3.38.0",
        sha256="73f43ef535929c6034982434aba4d5fd04db3b40f4e0cd14c3abfd56419d181d",
    )
    version(
        "3.37.0",
        sha256="242d6cffbd9e843af807487ff04853189b812081aeaa22f90a8f159f20220ed9",
    )

    depends_on("python@3.7:", type=["build", "run"])
    depends_on("py-setuptools", type="build")
