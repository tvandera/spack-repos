# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Ompss(Package):
    """OmpSs is an effort to integrate features from the StarSs programming
       model developed by BSC into a single programming model. In
       particular, our objective is to extend OpenMP with new directives
       to support asynchronous parallelism and heterogeneity (devices
       like GPUs). However, it can also be understood as new directives
       extending other accelerator based APIs like CUDA or OpenCL. Our
       OmpSs environment is built on top of our Mercurium compiler and
       Nanos++ runtime system.

    """
    homepage = "https://pm.bsc.es/"
    url      = "http://pm.bsc.es/sites/default/files/ftp/ompss/releases/ompss-14.10.tar.gz"
    list_url = 'https://pm.bsc.es/ompss-downloads'

    version('14.10', sha256='5b38d3e6ce108e7ca73a2599bc698d75ea9f6d90a3be0349faf6d61022e62a38')
    version('19.06', sha256='a3f513ebac6b8bcc8d6bc617428e871208dacf795a4c92b0db17d20497be2198')

    # all dependencies are optional, really
    depends_on("hwloc")
    depends_on("extrae")
    depends_on("sqlite")
    depends_on("libiconv")

    def install(self, spec, prefix):
        os.chdir(glob.glob('./nanox-*').pop())
        configure("--prefix=%s" % prefix,
                  "--with-mcc=%s" % prefix,
                  "--with-extrae=%s" % spec['extrae'].prefix,
                  "--with-hwloc=%s" % spec['hwloc'].prefix,
                  )
        make()
        make("install")

        os.chdir(glob.glob('../mcxx-*').pop())
        configure("--prefix=%s" % prefix,
                  "--with-nanox=%s" % prefix,
                  "--with-libiconv-prefix=%s" % spec['libiconv'].prefix,
                  "--enable-ompss",
                  "LDFLAGS=-liconv",
                 )
        make()
        make("install")
