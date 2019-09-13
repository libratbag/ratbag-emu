# SPDX-License-Identifier: MIT

from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ratbag-emu',
    version='0.0.1',
    description='Mouse emulation stack ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/libratbag/ratbag-emu',
    author='Filipe Laíns',
    author_email='lains@archlinux.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: System :: Emulators',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Operating System Kernels :: Linux',
    ],
    keywords='setuptools libratbag hardware mouse uhid emulation',
    project_urls={
        'Bug Reports': 'https://github.com/libratbag/ratbag-emu/issues',
        'Source': 'https://github.com/libratbag/ratbag-emu',
    },

    packages=[
        'ratbag_emu',
        'ratbag_emu.protocol',
        'ratbag_emu.protocol.devices',
        'ratbag_emu.protocol.util',
    ],
    install_requires=['hid-tools', 'connexion'],
    extras_require={
        'ui': ['connexion[swagger-ui]'],
        'test': ['libevdev']
    },
    test_requires=['pytest'],
    package_data={
        'openapi': ['src/ratbag_emu/openapi/ratbag-emu.yaml'],
    },
)
