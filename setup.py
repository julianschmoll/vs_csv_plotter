"""Sets up local workspace."""
# Import setuptools
from setuptools import find_packages, setup

setup(
    name='vs_csv_plotter',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'cachetools',
        'seaborn',
        'requests',
        'scipy'
    ],
)
