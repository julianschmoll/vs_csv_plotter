from setuptools import setup, find_packages

setup(
    name='vs_csv_plotter',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas==1.3.3',
        'matplotlib==3.4.3',
    ],
)