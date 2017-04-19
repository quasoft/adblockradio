#!/usr/bin/env python3
import os
from setuptools import setup, find_packages


def read_long_description():
    with open('README.txt') as f:
        return f.read()


osname = os.uname()[0]
if any([name for name in ['Darwin', 'Linux'] if osname in name]):
    data_files = [
        ('/usr/share/applications', ['share/adblockradio.desktop']),
        ('/usr/share/adblockradio', ['share/icon.svg'])
    ]
else:
    data_files = []


setup(
    name='adblockradio',
    version='0.3.2',
    author='QuaSoft',
    author_email='info@quasoft.net',
    description='Internet radio player for Ubuntu that blocks advertisements',
    long_description=read_long_description(),
    license='GPLv3',
    keywords='music internet radio player block advertisements',
    url='https://github.com/quasoft/adblockradio',
    packages=find_packages(),
    package_data={
        'adblockradio': [
            'adblockradio/ui/svg/*.svg'
        ]
    },
    include_package_data=True,
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'adblockradio=adblockradio.adblockradio:main'
        ]
    },
    download_url='https://github.com/quasoft/adblockradio/archive/0.3.2.tar.gz',
    install_requires=['appdirs', 'requests'],
    extras_require={
        'console':  ['plac']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Audio',
        'Topic :: Utilities'
    ]
)
