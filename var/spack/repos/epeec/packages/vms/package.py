from spack import *
import os
import glob

class Vms(MakefilePackage):
    """Virtual Molecule Screening"""

    homepage = "https://github.imec.be/vanderaa/epeec"
    git      = "git@github.imec.be:vanderaa/epeec.git"

    maintainers = ['tvandera', ]

    version('master',  branch='master')

    variant(
       'impl', default='plain', description='Implementation',
        values=( 'plain', 'omp', 'mpi', 'gpi', 'ompss'), multi=False,
    ) 

    depends_on('mpi', when='impl=mpi')
    depends_on('mpi', when='impl=gpi')
    depends_on('gpi-2+mpi', when='impl=gpi')

    depends_on('nanos6', when='impl=ompss')
    depends_on('mcxx', type='build', when='impl=ompss')

    build_directory = 'vms/pure_c'

    @property
    def build_targets(self):
        impl = self.spec.variants['impl'].value 
        return [ "-f", "Makefile." + impl ]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        binary = glob.glob(os.path.join(self.build_directory, '*', 'predict')).pop()
        install(binary, prefix.bin)
