# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.prefix import Prefix

import os
import glob


class Ompss2(Package):
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
    git      = "https://github.com/bsc-pm/ompss-2-releases"

    version('2021.06', tag='2021.06', submodules=True)

    conflicts('%gcc@7.4:')
    conflicts('%clang')
    depends_on('gcc@7.3.0')
    depends_on('nvhpc')
    depends_on('cuda')

    depends_on("hwloc")
    depends_on("extrae")
    depends_on("boost")
    depends_on("libunwind")
    depends_on("papi")
    depends_on("libiconv")
    depends_on("sqlite")

    depends_on("gperf", type="build")
    depends_on("autoconf", type='build')
    depends_on("automake", type='build')
    depends_on('pkgconfig', type='build')
    depends_on('libtool', type='build')

    # Requires GCC 


    def install(self, spec, prefix):
        nvhpc = spec['nvhpc']
        nvhpc_compiler_prefix = Prefix(join_path(nvhpc.prefix, 'Linux_%s' % nvhpc.target.family, nvhpc.version, 'compilers'))

        os.chdir(glob.glob('./nanos*').pop())
        autoreconf("--install", "--verbose", "--force")
        configure("--prefix=%s" % prefix,
                  "--with-papi=%s" % spec['papi'].prefix,
                  "--with-extrae=%s" % spec['extrae'].prefix,
                  "--with-libunwind=%s" % spec['libunwind'].prefix,
                  "--with-boost=%s" % spec['boost'].prefix,
                  "--enable-openacc",
                  "--with-pgi=%s" % nvhpc_compiler_prefix,
                  "--with-cuda=%s" % spec['cuda'].prefix,
        )
        make()
        make("install")

        os.chdir(glob.glob('../mcxx*').pop())
        autoreconf("--install", "--verbose", "--force")
        configure("--prefix=%s" % prefix,
                  "--enable-ompss-2",
                  "--with-libiconv-prefix=%s" % spec['libiconv'].prefix,
                  "--with-nanos6=%s" % prefix,
                  "--with-pgi-installation=%s" % nvhpc_compiler_prefix, 
                  "LDFLAGS=-liconv",
        )
        make()
        make("install")
