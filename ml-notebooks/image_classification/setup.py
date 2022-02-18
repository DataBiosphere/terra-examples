# Copyright 2021 Verily Life Sciences LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['cloudml-hypertune']

setup(
    name='trainer',
    version='0.7',
    python_requires='>=3.6',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='image classification training'
)
