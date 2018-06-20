# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name="alphacar", 
    version="1.0",
    description="alphacar blockchain SDK",
    url="https://www.alphacar.io",
    author="leo chen",
    author_email="leochan007@163.com",
    packages_dir=['src/alphacar'],
    package_data={'alphacar': ['keystore/*']},
    requires=['ipfsapi (>=0.4.3)', 'pymongo (>=3.6.1)', 'web3 (>=4.3.0)']
    )
