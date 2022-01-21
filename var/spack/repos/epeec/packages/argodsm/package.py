from spack import *

class Argodsm(CMakePackage):
    """ArgoDSM is a software distributed shared memory system.
    """

    homepage = "https://etascale.github.io/argodsm/"
    git      = "https://github.com/etascale/argodsm"

    maintainers = ['tvandera', ]

    version('2021.01', commit='24247b7bce2c184001142e8bcfda35b769bee4f5')
    version('epeec-final', branch='epeec-final-release', git='https://github.com/lundgren87/argodsm')

    depends_on('numactl')

    depends_on('mpi')

    resource(
        name='googletest',
        url='https://github.com/google/googletest/archive/release-1.7.0.zip',
        sha256='b58cb7547a28b2c718d1e38aee18a3659c9e3ff52440297e965f5edffe34b6d0',
        destination='tests',
        placement='gtest-1.7.0',
    )

    def cmake_args(self):
        define = CMakePackage.define
        args = [ 
            define('ARGO_ENABLE_MT', True),
            define('ARGO_TESTS', self.run_tests),
            define('CMAKE_CXX_COMPILER', self.spec['mpi'].mpicxx),
            define('CMAKE_C_COMPILER', self.spec['mpi'].mpicc),
        ]
        return args
