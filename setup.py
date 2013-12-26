import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="txswagger",
    version="0.1.dev",
    packages=find_packages(exclude=("tests.*", "tests")),

    author="The OpenNode Team",
    author_email="info@opennodecloud.com",

    maintainer="Ihor Kaharlichenko",
    maintainer_email="ihor@opennodecloud.com",

    description="Swagger Core library and Twisted Web integration",
    long_description=read('README.rst'),

    license="Apache2",
    url="https://github.com/opennode/txswagger",

    install_requires=[
        'twisted>=11.0',
    ],

    test_suite='tests',

    classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Networking",
    ],
)
