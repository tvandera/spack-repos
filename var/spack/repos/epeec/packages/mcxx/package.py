# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Mcxx(AutotoolsPackage):
    """OmpSs is an effort to integrate features from the StarSs programming
       model developed by BSC into a single programming model. In
       particular, our objective is to extend OpenMP with new directives
       to support asynchronous parallelism and heterogeneity (devices
       like GPUs). However, it can also be understood as new directives
       extending other accelerator based APIs like CUDA or OpenCL. Our
       OmpSs environment is built on top of our Mercurium compiler and
       Nanos++ runtime system.

    """
    homepage = "http://pm.bsc.es/"
    git      = "https://github.com/bsc-pm/mcxx"

    version('2021.11', tag='github-release-2021.11')


    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')

    depends_on('gcc@7.3.0')
    depends_on("nanos6")
    depends_on("hwloc")
    depends_on("extrae")
    depends_on("libiconv")
    depends_on("sqlite")
    depends_on("gperf", type="build")

    # requires gcc 7.x or lower
    conflicts('%gcc@8:')
    conflicts('%intel')
    conflicts('%clang')

    def configure_args(self):
        spec = self.spec
        return [
                  "--enable-ompss-2",
                  "--with-libiconv-prefix=%s" % spec['libiconv'].prefix,
                  "--with-nanos6=%s" % spec['nanos6'].prefix,
                  "LDFLAGS=-liconv",
        ]
