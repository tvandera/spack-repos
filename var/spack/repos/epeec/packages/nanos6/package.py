# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.prefix import Prefix


class Nanos6(AutotoolsPackage):
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
    git      = "https://github.com/bsc-pm/nanos6"

    version('2021.11', tag='github-release-2021.11')

    version('argodsm', branch='cluster-argo', git="https://github.com/epeec/nanos6-argodsm")
    version('cluster', commit='dce396554ea2645ebf23cb6a16c65a42a83e1221', git="https://github.com/bsc-pm/nanos6-cluster")
    version('openacc', branch='device-affinity', git="git@github.com:orestiskor/nanos6-openacc.git")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')
    depends_on("gperf", type="build")

    depends_on("argodsm@epeec-final", when='@argodsm')
    depends_on("mpi", when='@cluster')

    depends_on('gcc',   when="@openacc", type=('build', 'run'))
    depends_on('nvhpc', when="@openacc", type=('build', 'run'))
    depends_on('cuda',  when="@openacc")

    depends_on("hwloc")
    depends_on("extrae")
    depends_on("boost")
    depends_on("libunwind")
    depends_on("papi")
    depends_on("libiconv")
    depends_on("sqlite")

    patch("debug_multiGPU.patch", when="@openacc")

    def configure_args(self):
        spec = self.spec
        args = [
                  "--with-papi=%s" % spec['papi'].prefix,
                  "--with-extrae=%s" % spec['extrae'].prefix,
                  "--with-libunwind=%s" % spec['libunwind'].prefix,
                  "--with-boost=%s" % spec['boost'].prefix,
        ]

        if '^argodsm' in spec:
            args += [ '--with-argodsm=%s' % spec['argodsm'].prefix ]
            args += [ '--enable-cluster' ]

        if '@cluster' in spec:
            args += [ '--enable-cluster' ]

        if '@openacc' in spec:
            nvhpc = spec['nvhpc']
            nvhpc_compiler_prefix = Prefix(join_path(nvhpc.prefix, 'Linux_%s' % nvhpc.target.family, nvhpc.version, 'compilers'))
            args += [
                  "--enable-openacc",
                  "--with-pgi=%s" % nvhpc_compiler_prefix,
                  "--with-cuda=%s" % spec['cuda'].prefix,
            ]

        return args