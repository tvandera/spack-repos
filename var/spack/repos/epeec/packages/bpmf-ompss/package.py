from spack import *
import spack.util
import os

class BpmfOmpss(MakefilePackage):
    """Julia and C++ implementations of Bayesian Probabilistic Matrix
    Factorization using Markov Chain Monte Carlo."""

    homepage = "https://github.com/ExaScience/bpmf"
    git      = "https://github.com/ExaScience/bpmf"

    maintainers = ['tvandera', ]

    version('ompss',  branch='ompss')

    # numlatent = [2, 4, 8, ..., 128]
    variant(
       'nl', default='64', description='number of latent dimensions',
        values=[ str(2**i) for i in range(1,8) ], multi=False
    )

    depends_on('nanos6')
    depends_on('mcxx', type='build')

    # common bpmf dependecies
    depends_on('random123')
    depends_on('eigen')
    depends_on('zlib')

    build_directory = 'makefiles'

    @property
    def build_targets(self):
        args = [
            "bpmf",
            "BPMF_NUMLATENT=%s" % self.spec.variants['nl'].value,
        ]


        if "nanos6@argodsm" in self.spec:
            args.append("CLUSTER_BACKEND=ARGO")

        return args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(os.path.join(self.build_directory, 'bpmf'), os.path.join(prefix.bin, 'bpmf'))
        # for file in [ 'mcc_bpmf', 'extrae.xml', 'nanos6.toml', 'trace.sh' ]:
        #    install(os.path.join(self.build_directory, file), prefix.bin)
