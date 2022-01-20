from spack import *

class Argodsm(CMakePackage):
    """ArgoDSM is a software distributed shared memory system.
    """

    homepage = "https://etascale.github.io/argodsm/"
    git      = "https://github.com/etascale/argodsm"

    maintainers = ['tvandera', ]

    version('2021.01', commit='24247b7bce2c184001142e8bcfda35b769bee4f5')

    depends_on('numactl')
    depends_on('mpi')
    depends_on('googletest@1.7.0', type='test')

    @run_before('cmake')
    def link_google_test(self):
        if self.run_tests:
            import os
            # see instructions on https://etascale.github.io/argodsm/
            os.symlink(self.spec['googletest'].prefix, 'gtest-1.7.0')

    def cmake_args(self):
        define = CMakePackage.define
        args = [ 
            define('ARGO_ENABLE_MT', True),
            define('ARGO_TESTS', self.run_tests),
        ]
        return args
