import os
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read().strip()


setup(
    name='cloudwise',
    version='0.1.1',
    author='Surreal AI',
    url='http://github.com/SurrealAI/cloudwise',
    description='Set up a Kubernetes cluster for distributed AI research',
    long_description=read('README.rst'),
    keywords=['machine learning',
              'cloud computing',
              'distributed computing',
              'terraform',
              'kubernetes'],
    license='GPLv3',
    packages=[
        package for package in find_packages() if package.startswith("cloudwise")
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3"
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={
        'console_scripts': ['cloudwise-gke=cloudwise.gke.gke_commandline:main'],
    },
    python_requires='>=3.5',
)
