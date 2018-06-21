# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

packages = ['alphacar']

requires = [
    'ipfsapi==0.4.3',
    'pymongo==3.6.1',
    'web3==4.2.0',
]

setup(
    name="alphacar",
    version="1.0",
    description="alphacar blockchain SDK",
    author="leo chen",
    author_email="leochan007@163.com",
    
    license="MIT",
    keywords="alphacar blockchain",
    url="https://www.alphacar.io",
    #scripts=['say_hello.py'],

    packages=packages,
    package_dir={'alphacar': 'src/alphacar'},
    package_data={'': ['LICENSE'], 'alphacar': ['keystore/*']},
    include_package_data=True,
    zip_safe=False,
    
    install_requires=requires,
)
