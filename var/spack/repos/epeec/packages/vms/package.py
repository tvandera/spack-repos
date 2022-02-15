from spack import *
import os

class Vms(MakefilePackage):
    """Virtual Molecule Screening"""

    homepage = "https://github.imec.be/vanderaa/epeec"
    git      = "git@github.imec.be:vanderaa/epeec.git"

    maintainers = ['tvandera', ]

    version('master',  branch='master')

    variant('mpi', default=False)
    variant('ompss', default=False)

    depends_on('nanos6', when='+ompss')
    depends_on('mpi', when='+mpi')
    depends_on('mcxx', type='build', when='+ompss')

    build_directory = 'vms/pure_c'

    @property
    def build_targets(self):
        args = [ "predict", ]

        if "+mpi" in self.spec:
            args += [
                'CFLAGS=-DUSE_MPI',
                'LDFLAGS=-lmpi',
            ]

        if "+ompss" in self.spec:
            args += [
                'CFLAGS=--ompss-2 -DOMPSS',
                'CC=mcc',
            ]

        return args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(os.path.join(self.build_directory, 'predict'), os.path.join(prefix.bin, 'predict'))
