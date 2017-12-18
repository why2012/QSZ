# coding: utf-8
def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    return config

def setup_package():
    import sys
    deps = [
            'numpy',
            'MySQL-python',
            'tornado',
            'requests',
            'pycrypto'
        ]

    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
        install_requires=deps,
    )
    
    metadata = dict(name="QSZ_DEP",
                    maintainer="w.h.y.",
                    maintainer_email="529570509@qq.com",
                    description="dependency",
                    license="all rights reserved.",
                    url="",
                    download_url="",
                    version="0.0.1",
                    long_description="dependency",
                    **extra_setuptools_args)

    from numpy.distutils.core import setup

    metadata['configuration'] = configuration
    setup(**metadata)   

if __name__ == "__main__":
    setup_package()