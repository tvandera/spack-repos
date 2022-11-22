from spack.package import *
import os

class Bpmf(CMakePackage):
    """Julia and C++ implementations of Bayesian Probabilistic Matrix
    Factorization using Markov Chain Monte Carlo."""

    homepage = "https://github.com/ExaScience/bpmf"
    git      = "https://github.com/ExaScience/bpmf"

    maintainers = ['tvandera', ]

    version('ompss',  branch='ompss')
    version('master', branch='master')

    # numlatent = [2, 4, 8, ..., 128]
    variant(
       'nl', default='64', description='number of latent dimensions',
        values=[ str(2**i) for i in range(1,8) ], multi=False
    )

    variant('profile', default=True, description='Enable profiling')
    variant('asan', default=False, description='Enable address sanitizer')
    variant('tsan', default=False, description='Enable thread sanitizer')

    mpi_comms = ( 'mpi_isend', 'mpi_bcast', 'mpi_put', 'gpi' )
    variant(
       'comm', default='no', description='Communication library',
        values=mpi_comms + ( 'argo', 'no'), multi=False,
        when="@master"
    )

    for c in mpi_comms:
        depends_on('mpi', when=f"comm={c}")

    depends_on('cmake', type='build')
    depends_on('gpi-2+mpi', when="comm=gpi")
    depends_on('argodsm', when="comm=argo")

    depends_on('mpi', type="test")

    depends_on('random123')
    depends_on('eigen')
    depends_on('zlib')

    def cmake_args(self):
        args = [
            self.define('BPMF_COMM', self.spec.variants['comm'].value.upper() + "_COMM"),
            self.define('BPMF_NUMLATENT', self.spec.variants['nl'].value),
            self.define_from_variant('ENABLE_ASAN', 'asan'),
            self.define_from_variant('ENABLE_TSAN', 'tsan'),
            self.define_from_variant('ENABLE_PROFILING', 'profile'),
        ]

        return args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(os.path.join(self.build_directory, 'bpmf'), prefix.bin)
