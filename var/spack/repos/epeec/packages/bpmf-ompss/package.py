from spack import *
import spack.util
import os

class BpmfOmpss(MakefilePackage):
    """Julia and C++ implementations of Bayesian Probabilistic Matrix
    Factorization using Markov Chain Monte Carlo."""

    homepage = "https://github.com/ExaScience/bpmf"
    git      = "https://github.com/ExaScience/bpmf"

    maintainers = ['tvandera', ]

    version('argo',  branch='ompss@argo')
    version('cluster',  branch='ompss@cluster')

    # numlatent = [2, 4, 8, ..., 128]
    variant(
       'nl', default='64', description='number of latent dimensions',
        values=[ str(2**i) for i in range(1,8) ], multi=False
    )

    variant('profile', default=True, description='Enable profiling')

    depends_on('nanos6@argodsm', when='@argo')
    depends_on('nanos6@cluster', when='@cluster')
    depends_on('mcxx', type='build')

    # common bpmf dependecies
    depends_on('random123')
    depends_on('eigen')
    depends_on('zlib')

    build_directory = 'makefiles'

    @property
    def build_targets(self):
        return [
            "mcc_bpmf",
            "BPMF_NUMLATENT=%s" % self.spec.variants['nl'].value,
        ]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        for file in [ 'mcc_bpmf', 'extrae.xml', 'nanos6.toml', 'trace.sh' ]:
            install(os.path.join(self.build_directory, file), prefix.bin)