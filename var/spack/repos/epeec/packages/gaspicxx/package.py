from spack.package import *

class Gaspicxx(CMakePackage):
    """GaspiCxx is a C++ interface for the communication library GPI-2"""

    homepage = "https://github.com/cc-hpc-itwm/GaspiCxx"
    url      = "https://github.com/cc-hpc-itwm/GaspiCxx/archive/refs/tags/v1.0.0.tar.gz"
    git      = "https://github.com/cc-hpc-itwm/GaspiCxx.git"

    maintainers = ['tvandera']

    version('1.0.0', sha256='b40cc46517d5174b91a419e4181f2ec958dada22ab046be1f64d9aec97b5ecbc')

    depends_on('cmake @3.10:', type='build')
    depends_on('googletest', type='build')
    depends_on('gpi-2 @1.4.0:')

    def cmake_args(self):
        args = [
              '-DENABLE_TEST=ON',
        ]

        return args

