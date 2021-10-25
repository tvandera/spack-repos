# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob


class Ompss2Cluster(Package):
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
    git      = "https://github.com/bsc-pm/ompss-2-cluster-releases"

    version('2021.05', tag='2021.05', submodules=True)

    depends_on('gcc@7.3.0')
    depends_on("mpi")
    depends_on("hwloc")
    depends_on("extrae")
    depends_on("boost")
    depends_on("libunwind")
    depends_on("papi")
    depends_on("libiconv")
    depends_on("sqlite")
    depends_on("gperf", type="build")

    def install(self, spec, prefix):
        os.chdir(glob.glob('./nanos*').pop())
        autoreconf("--install", "--verbose", "--force")
        configure("--prefix=%s" % prefix,
                  "--with-papi=%s" % spec['papi'].prefix,
                  "--with-extrae=%s" % spec['extrae'].prefix,
                  "--with-libunwind=%s" % spec['libunwind'].prefix,
                  "--with-boost=%s" % spec['boost'].prefix,
                  "--enable-cluster",
        )
        make()
        make("install")

        os.chdir(glob.glob('../mcxx*').pop())
        autoreconf("--install", "--verbose", "--force")
        configure("--prefix=%s" % prefix,
                  "--enable-ompss-2",
                  "--with-libiconv-prefix=%s" % spec['libiconv'].prefix,
                  "--with-nanos6=%s" % prefix,
                  "LDFLAGS=-liconv",
        )
        make()
        make("install")
